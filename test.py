# coding:utf-8
import os
import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from glv import Icon, Param, MergePath, BeautifyStyle, FileStatus
from ui_class.ProjectBar import ProjectBar
from ui_class.EditorTab import EditorTab
from ui_class.New import New

'''
需要增加的功能:
1.块导入
2.点击跳转
'''


# 窗口app
class MainWindow(QMainWindow):
    def __init__(self, parent=None, title='未命名'):
        super(MainWindow, self).__init__(parent)
        self.setGeometry(100, 100, 1000, 700)
        self.setWindowTitle(title)
        # 样式美化
        main_ui_style = BeautifyStyle.font_family + BeautifyStyle.font_size + BeautifyStyle.file_dialog_qss
        self.setStyleSheet(main_ui_style)
        # 中间widget区域
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        # 工程栏
        self.project_path = MergePath(os.getcwd()).merged_path
        self.project_bar = ProjectBar(self.central_widget, self.project_path)
        self.project_bar.signal[str].connect(self.get_signal_from_project_bar)
        # 编辑器设置
        # self.editor = MyQscintilla(self.centralWidget())
        # self.setCentralWidget(self.editor)
        self.editor_widget = EditorTab(self.central_widget)
        self.editor_widget.signal[str].connect(self.get_signal_from_editor)
        # self.setCentralWidget(self.editor_widget)
        # 全局竖直布局
        self.general_v_layout = QVBoxLayout(self.central_widget)
        self.general_v_layout.setContentsMargins(1, 0, 0, 0)
        # 分割窗口布局
        self.splitter_h_general = QSplitter(Qt.Horizontal)
        self.splitter_h_general.setHandleWidth(0)
        self.splitter_h_general.addWidget(self.project_bar)
        self.splitter_h_general.addWidget(self.editor_widget)
        # 按比例分割
        # self.splitter_h_general.setStretchFactor(0, 1)
        # self.splitter_h_general.setStretchFactor(1, 4)
        # 按尺寸分割
        self.splitter_h_general.setSizes([200, 800])
        self.general_v_layout.addWidget(self.splitter_h_general)
        self.setLayout(self.general_v_layout)
        # 菜单栏
        self.menu_bar = QMenuBar(self)
        self.menu_bar.setObjectName('menu_bar')
        # 设置菜单栏样式
        menu_style = 'QMenu::item {background-color: transparent; padding-left: 5px; padding-right: 5px;}\
                      QMenu::item:selected {background-color: #2DABF9;}'
        self.menu_bar.setStyleSheet(menu_style)
        self.setMenuBar(self.menu_bar)
        # 菜单和工具--功能action
        self.new_action = QAction(QIcon(Icon.new), '打开文件夹(Alt+N)', self)
        self.new_action.setShortcut('ctrl+alt+n')
        self.new_action.triggered.connect(self.connect_new)
        self.open_folder_action = QAction(QIcon(Icon.open_folder), '打开文件夹(Shift+O)', self)
        self.open_folder_action.setShortcut('ctrl+shift+o')
        self.open_folder_action.triggered.connect(self.connect_open_folder)
        self.open_file_action = QAction(QIcon(Icon.open_file), '打开文件(O)', self)
        self.open_file_action.setShortcut('ctrl+o')
        self.open_file_action.triggered.connect(self.connect_open_file)
        self.save_file_action = QAction(QIcon(Icon.save_file), '保存文件(S)', self)
        self.save_file_action.setShortcut('ctrl+s')
        self.save_file_action.triggered.connect(self.connect_save_file)
        self.save_as_file_action = QAction(QIcon(Icon.save_as_file), '另存文件为(Shift+S)', self)
        self.save_as_file_action.setShortcut('ctrl+shift+s')
        self.save_as_file_action.triggered.connect(self.connect_save_as_file)
        # 文件菜单栏
        self.file_bar = self.menu_bar.addMenu('文件')
        self.file_bar.addAction(self.new_action)
        self.file_bar.addAction(self.open_folder_action)
        self.file_bar.addAction(self.open_file_action)
        self.file_bar.addAction(self.save_file_action)
        self.file_bar.addAction(self.save_as_file_action)
        # 帮助菜单栏
        self.help_bar = self.menu_bar.addMenu('帮助')
        self.help_action_menu = QAction('操作说明', self)
        # self.help_action_menu.triggered.connect(self.connect_open_file)
        self.help_bar.addAction(self.help_action_menu)
        # 工具栏
        self.tool_bar = self.addToolBar('tool_bar')
        self.tool_bar.addAction(self.new_action)
        self.tool_bar.addAction(self.open_folder_action)
        self.tool_bar.addAction(self.open_file_action)
        self.tool_bar.addAction(self.save_file_action)
        self.tool_bar.addAction(self.save_as_file_action)
        # 状态栏 & 状态栏显示
        self.status_bar = QStatusBar(self)
        self.status_bar.setObjectName('status_bar')
        self.status_bar.setContentsMargins(0, 0, 0, 0)
        self.setStatusBar(self.status_bar)
        # 状态栏内控件
        self.file_icon = QToolButton(self)
        self.file_icon.setStyleSheet('QToolButton{border-image: url(' + Icon.file + ')}')
        self.file_path_label = QLabel(self)
        self.file_path_label.setText('')
        self.file_status_label = QLabel(self)
        self.file_status_label.setText('')
        self.cursor_label = QLabel(self)
        self.cursor_label.setText('')
        # 状态栏布局
        self.status_bar.addPermanentWidget(self.file_icon, stretch=0)
        self.status_bar.addPermanentWidget(self.file_path_label, stretch=0)
        self.status_bar.addPermanentWidget(self.file_status_label, stretch=1)
        self.status_bar.addPermanentWidget(self.cursor_label, stretch=1)

    # 获取编辑器文本中发出的信号
    def get_signal_from_editor(self, signal_str):
        flag = signal_str.split('>')[0]
        # 状态-文件路径
        if flag == 'file_path':
            file_path = signal_str.split('>')[1]
            self.file_path_label.setText(file_path)
        # 状态-光标位置
        elif flag == 'cursor_position':
            cursor_position = signal_str.split('>')[1]
            self.cursor_label.setText(cursor_position)
        # 状态-文件保存状态
        elif flag == 'file_status':
            index = self.editor_widget.currentIndex()
            file_status = self.editor_widget.file_status_list[index]
            self.file_status_label.setText(file_status)
        else:
            pass

    # 获取工程栏发出的信号
    def get_signal_from_project_bar(self, signal_str):
        flag = signal_str.split('>')[0]
        path = signal_str.split('>')[1]
        if flag == 'open_xml':
            self.editor_widget.open_edit_tab(path)
        elif flag == 'delete_path':
            if path in self.editor_widget.file_list:
                index = self.editor_widget.file_list.index(path)
                self.close_tab(index)

    # 获取New文件系统发出的信号
    def get_signal_from_new(self, signal_str):
        flag = signal_str.split('>')[0]
        path = signal_str.split('>')[1]
        # 文件新建、打开、等等操作
        if os.path.exists(path):
            self.project_bar.update_select_item(path)
            self.project_bar.operation_file(path)
        # 文件删除操作
        else:
            if path in self.editor_widget.file_list:
                index = self.editor_widget.file_list.index(path)
                self.close_tab(index)

    # 新建(可以选择文件/文件夹)
    def connect_new(self):
        # 新建菜单(可新建 文件/文件夹/xml文件)
        self.new_dialog = New(self, os.getcwd())
        self.new_dialog.signal[str].connect(self.get_signal_from_new)
        self.new_dialog.exec()

    # 打开文件夹
    def connect_open_folder(self):
        print('打开文件夹')

    # 打开文件
    def connect_open_file(self):
        self.editor_widget.open_edit_tab()

    # 保存文件
    def connect_save_file(self):
        self.editor_widget.save_edit_tab()

    # 另存文件为
    def connect_save_as_file(self):
        self.editor_widget.save_file_as_tab()

    # 删除文件后关闭tab页面
    def close_tab(self, index):
        # 删除tab栏
        self.editor_widget.removeTab(index)
        self.editor_widget.file_list.pop(index)
        self.editor_widget.file_status_list.pop(index)
        # 删除完tab后需要修改状态栏
        tab_counts = self.editor_widget.count()
        if tab_counts > 0:
            new_index = self.editor_widget.currentIndex()
            file_path = self.editor_widget.file_list[new_index]
            cursor_position = '[0:0]'
            self.get_signal_from_editor('file_path>' + file_path)
            self.get_signal_from_editor('cursor_position>' + cursor_position)
        else:
            file_path = 'None'
            cursor_position = '[0:0]'
            self.get_signal_from_editor('file_path>' + file_path)
            self.get_signal_from_editor('cursor_position>' + cursor_position)

    # 窗口关闭事件
    def closeEvent(self, event):
        close_flag = True
        for file_status in self.editor_widget.file_status_list:
            if file_status == FileStatus.not_save_status:
                close_flag = False
                index = self.editor_widget.file_status_list.index(file_status)
                file = self.editor_widget.file_list[index]
                break
        if close_flag is True:
            event.accept()
        else:
            reply = QMessageBox.question(self, '有文件未保存', file+'未保存\n是否先保存文件？', QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.No)
            if reply == QMessageBox.No:
                event.accept()
            elif reply == QMessageBox.Cancel:
                event.ignore()
            elif reply == QMessageBox.Yes:
                with open(file, 'w', encoding='utf-8') as f:
                    text = self.editor_widget.widget(index).text()
                    f.write(text)
                    event.accept()
            else:
                event.ignore()


if __name__=='__main__':
    '''将QFileDialog转为中文'''
    tran = QTranslator()
    tran.load(Param.translator_file)
    app = QApplication(sys.argv)
    app.installTranslator(tran)
    form = MainWindow(None, 'xml-editor')
    form.show()
    app.exec_()

    '''未将QFileDialog转为中文'''
    # app = QApplication(sys.argv)
    # form = MainWindow(None, 'xml-editor')
    # form.show()
    # app.exec_()