# coding:utf-8
import os
import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from glv import Icon, MergePath
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
        self.setFont(QFont('Consolas', 14, QFont.Bold))
        # 中间widget区域
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        # 工程栏
        self.project_path = MergePath(os.getcwd()).merged_path
        self.project_bar = ProjectBar(self.central_widget, self.project_path)
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
        self.splitter_h_general.setStretchFactor(0, 1)
        self.splitter_h_general.setStretchFactor(1, 4)
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
        # 文件菜单栏
        self.file_bar = self.menu_bar.addMenu('文件')
        self.new_file_action_menu = QAction('新建文件', self)
        self.new_file_action_menu.triggered.connect(self.connect_new_file)
        self.open_file_action_menu = QAction('打开文件', self)
        self.open_file_action_menu.triggered.connect(self.connect_open_file)
        self.save_file_action_menu = QAction('保存文件', self)
        self.save_file_action_menu.triggered.connect(self.connect_save_file)
        self.file_bar.addAction(self.new_file_action_menu)
        self.file_bar.addAction(self.open_file_action_menu)
        self.file_bar.addAction(self.save_file_action_menu)
        # 帮助菜单栏
        self.help_bar = self.menu_bar.addMenu('帮助')
        self.help_action_menu = QAction('操作说明', self)
        # self.help_action_menu.triggered.connect(self.connect_open_file)
        self.help_bar.addAction(self.help_action_menu)
        # 工具栏
        self.tool_bar = self.addToolBar('tool_bar')
        self.new_file_action = QAction(QIcon(Icon.new_file), '新建文件', self)
        self.new_file_action.triggered.connect(self.connect_new_file)
        self.open_file_action = QAction(QIcon(Icon.open_file), '打开文件', self)
        self.open_file_action.triggered.connect(self.connect_open_file)
        self.save_file_action = QAction(QIcon(Icon.save_file), '保存文件', self)
        self.save_file_action.triggered.connect(self.connect_save_file)
        self.tool_bar.addAction(self.new_file_action)
        self.tool_bar.addAction(self.open_file_action)
        self.tool_bar.addAction(self.save_file_action)
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

    # 新建文件
    def connect_new_file(self):
        self.editor_widget.new_edit_tab()

    # 打开文件
    def connect_open_file(self):
        self.editor_widget.open_edit_tab()

    # 保存文件
    def connect_save_file(self):
        self.editor_widget.save_edit_tab()

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
    app = QApplication(sys.argv)
    form = MainWindow(None, 'xml-editor')
    form.show()
    app.exec_()