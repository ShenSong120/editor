# coding:utf-8
import os
import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from glv import Icon, Param, MergePath, BeautifyStyle
from ui_class.ProjectBar import ProjectBar
from ui_class.EditorTab import EditorTab

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
        # 菜单栏
        self.menu_bar = QMenuBar(self)
        self.menu_bar.setObjectName('menu_bar')
        # 设置菜单栏样式
        menu_style = 'QMenu::item {background-color: transparent; padding-left: 5px; padding-right: 5px;}\
                              QMenu::item:selected {background-color: #2DABF9;}'
        self.menu_bar.setStyleSheet(menu_style)
        self.setMenuBar(self.menu_bar)
        # 菜单和工具--功能action
        self.open_file_action = QAction(QIcon(Icon.open_file), '打开文件(O)', self)
        self.open_file_action.setShortcut('ctrl+o')
        self.open_file_action.triggered.connect(self.connect_open_file)
        self.save_file_action = QAction(QIcon(Icon.save_file), '保存文件(S)', self)
        self.save_file_action.setShortcut('ctrl+s')
        self.save_file_action.triggered.connect(self.connect_save_file)
        self.save_as_file_action = QAction(QIcon(Icon.save_as_file), '另存文件为(Alt+S)', self)
        self.save_as_file_action.setShortcut('ctrl+alt+s')
        self.save_as_file_action.triggered.connect(self.connect_save_as_file)
        # 文件菜单栏
        self.file_bar = self.menu_bar.addMenu('文件')
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
        self.file_path_label.setText('new.xml')
        self.cursor_label = QLabel(self)
        self.cursor_label.setText('[1:1]')
        # 状态栏布局
        self.status_bar.addPermanentWidget(self.file_icon, stretch=0)
        self.status_bar.addPermanentWidget(self.file_path_label, stretch=5)
        self.status_bar.addPermanentWidget(self.cursor_label, stretch=1)

    # 获取编辑器文本中发出的信号
    def get_signal_from_editor(self, signal_str):
        flag = signal_str.split('>')[0]
        if flag == 'file_path':
            file_path = signal_str.split('>')[1]
            self.file_path_label.setText(file_path)
        elif flag == 'cursor_position':
            cursor_position = signal_str.split('>')[1]
            self.cursor_label.setText(cursor_position)
        else:
            pass

    # 获取工程栏发出的信号
    def get_signal_from_project_bar(self, signal_str):
        flag = signal_str.split('>')[0]
        file_path = signal_str.split('>')[1]
        if flag == 'open_xml':
            self.editor_widget.open_edit_tab(file_path)
        elif flag == 'new_xml':
            self.editor_widget.new_edit_tab(file_path)
        elif flag == 'delete':
            if file_path in self.editor_widget.file_list:
                index = self.editor_widget.file_list.index(file_path)
                self.close_tab(index)

    # 删除文件后关闭tab页面
    def close_tab(self, index):
        # 删除tab栏
        self.editor_widget.removeTab(index)
        self.editor_widget.file_list.pop(index)
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

    # 打开文件
    def connect_open_file(self):
        self.editor_widget.open_edit_tab()

    # 保存文件
    def connect_save_file(self):
        self.editor_widget.save_edit_tab()

    # 另存文件为
    def connect_save_as_file(self):
        self.editor_widget.save_file_as_tab()

    # 窗口关闭事件
    def closeEvent(self, event):
        close_flag = True
        for file in self.editor_widget.file_list:
            if os.path.exists(file) is False:
                close_flag = False
                break
        if close_flag is True:
            event.accept()
        else:
            reply = QMessageBox.question(self, '当前工程还有未保存文件', '是否先保存文件？', QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.No)
            if reply == QMessageBox.No:
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