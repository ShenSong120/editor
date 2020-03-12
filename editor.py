# coding:utf-8
import os
import sys
import json
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from other.glv import Icon, Param, MergePath, BeautifyStyle, FileStatus, EditorAction
from ui_class.ProjectBar import ProjectBar
from ui_class.EditorTab import EditorTab
from ui_class.New import New
from other.CaseConfigParser import CaseConfigParser

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
        self.cf = CaseConfigParser()
        self.cf.read(Param.config_file, encoding='utf-8')
        self.project_path = Param.project_path = MergePath(self.cf.get('default', 'project_path')).merged_path
        self.project_bar = ProjectBar(self.central_widget, self.project_path)
        self.project_bar.signal[str].connect(self.get_signal_from_project_bar)
        # 编辑器设置
        self.editor_widget = EditorTab(self.central_widget)
        self.editor_widget.signal[str].connect(self.get_signal_from_editor)
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
        self.new_action = QAction(QIcon(Icon.new), '新建(Alt+N)', self)
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
        # 编辑操作动作
        self.undo_action = QAction(QIcon(Icon.undo), '撤消上一次操作(Ctrl+Z)', self)
        self.undo_action.triggered.connect(self.connect_undo)
        self.redo_action = QAction(QIcon(Icon.redo), '恢复上一次操作(Ctrl+Y)', self)
        self.redo_action.triggered.connect(self.connect_redo)
        self.cut_action = QAction(QIcon(Icon.cut), '剪切(Ctrl+X)', self)
        self.cut_action.triggered.connect(self.connect_cut)
        self.copy_action = QAction(QIcon(Icon.copy), '复制(Ctrl+C)', self)
        self.copy_action.triggered.connect(self.connect_copy)
        self.paste_action = QAction(QIcon(Icon.paste), '粘贴(Ctrl+V)', self)
        self.paste_action.triggered.connect(self.connect_paste)
        self.delete_action = QAction(QIcon(Icon.delete), '删除(Backspace)', self)
        self.delete_action.triggered.connect(self.connect_delete)
        self.select_all_action = QAction(QIcon(Icon.select_all), '选中全部(Ctrl+A)', self)
        self.select_all_action.triggered.connect(self.connect_select_all)
        self.comment_action = QAction(QIcon(Icon.comment), '添加/去除-注释(Ctrl+/)', self)
        self.comment_action.triggered.connect(self.connect_comment)
        self.search_action = QAction(QIcon(Icon.search), '搜索(Ctrl+F)', self)
        self.search_action.triggered.connect(self.connect_search)
        self.replace_action = QAction(QIcon(Icon.replace), '替换(Ctrl+R)', self)
        self.replace_action.triggered.connect(self.connect_replace)
        # 非使能编辑操作动作
        self.set_edit_tool_bar_enable(status=False)
        # 文件菜单栏
        self.file_menu_bar = self.menu_bar.addMenu('文件')
        self.file_menu_bar.addAction(self.new_action)
        self.file_menu_bar.addAction(self.open_folder_action)
        self.file_menu_bar.addAction(self.open_file_action)
        self.file_menu_bar.addAction(self.save_file_action)
        self.file_menu_bar.addAction(self.save_as_file_action)
        # 编辑菜单栏
        self.edit_menu_bar = self.menu_bar.addMenu('编辑')
        self.edit_menu_bar.addAction(self.undo_action)
        self.edit_menu_bar.addAction(self.redo_action)
        self.edit_menu_bar.addAction(self.cut_action)
        self.edit_menu_bar.addAction(self.copy_action)
        self.edit_menu_bar.addAction(self.paste_action)
        self.edit_menu_bar.addAction(self.delete_action)
        self.edit_menu_bar.addAction(self.select_all_action)
        self.edit_menu_bar.addAction(self.comment_action)
        self.edit_menu_bar.addAction(self.search_action)
        self.edit_menu_bar.addAction(self.replace_action)
        # 帮助菜单栏
        self.help_menu_bar = self.menu_bar.addMenu('帮助')
        self.help_action = QAction('操作说明', self)
        # self.help_action.triggered.connect(self.connect_open_file)
        self.help_menu_bar.addAction(self.help_action)
        # 文件工具栏
        self.file_tool_bar = self.addToolBar('file_tool_bar')
        self.file_tool_bar.setMaximumHeight(32)
        self.file_tool_bar.addAction(self.new_action)
        self.file_tool_bar.addAction(self.open_folder_action)
        self.file_tool_bar.addAction(self.open_file_action)
        self.file_tool_bar.addAction(self.save_file_action)
        self.file_tool_bar.addAction(self.save_as_file_action)
        # 编辑工具栏
        self.edit_tool_bar = self.addToolBar('edit_tool_bar')
        self.edit_tool_bar.setMaximumHeight(32)
        self.edit_tool_bar.addAction(self.undo_action)
        self.edit_tool_bar.addAction(self.redo_action)
        self.edit_tool_bar.addAction(self.cut_action)
        self.edit_tool_bar.addAction(self.copy_action)
        self.edit_tool_bar.addAction(self.paste_action)
        self.edit_tool_bar.addAction(self.delete_action)
        self.edit_tool_bar.addAction(self.select_all_action)
        self.edit_tool_bar.addAction(self.comment_action)
        self.edit_tool_bar.addAction(self.search_action)
        self.edit_tool_bar.addAction(self.replace_action)
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
        self.status_bar.addPermanentWidget(self.cursor_label, stretch=7)

    # 设置编辑器动作是否使能(默认不使能)
    def set_edit_tool_bar_enable(self, status=False):
        self.undo_action.setEnabled(status)
        self.redo_action.setEnabled(status)
        self.cut_action.setEnabled(status)
        self.copy_action.setEnabled(status)
        self.paste_action.setEnabled(status)
        self.delete_action.setEnabled(status)
        self.select_all_action.setEnabled(status)
        self.comment_action.setEnabled(status)
        self.search_action.setEnabled(status)
        self.replace_action.setEnabled(status)

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
        # 函数跳转
        elif flag == 'dump_in_function':
            file_path = signal_str.split('>')[1]
            self.editor_widget.open_edit_tab(file_path)
        # 更新工具栏动作状态
        elif flag == 'action':
            self.update_tool_bar_enable_status(signal_str.split('>')[1])
        # 关闭所有子tab信号
        elif flag == 'close_all_tab':
            self.set_edit_tool_bar_enable(status=False)
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

    # 更新工具栏动作状态
    def update_tool_bar_enable_status(self, signal_str):
        edit_tool_bar_action_enable_status_dict = json.loads(signal_str)
        enable_status, disable_status = 'true', 'false'
        action_dict = {EditorAction.undo: self.undo_action,
                       EditorAction.redo: self.redo_action,
                       EditorAction.cut: self.cut_action,
                       EditorAction.copy: self.copy_action,
                       EditorAction.paste: self.paste_action,
                       EditorAction.delete: self.delete_action,
                       EditorAction.select_all: self.select_all_action,
                       EditorAction.comment: self.comment_action,
                       EditorAction.search: self.search_action,
                       EditorAction.replace: self.replace_action}
        for action in action_dict.keys():
            if edit_tool_bar_action_enable_status_dict[action] == enable_status:
                action_dict[action].setEnabled(True)
            elif edit_tool_bar_action_enable_status_dict[action] == disable_status:
                action_dict[action].setEnabled(False)

    # 新建(可以选择文件/文件夹)
    def connect_new(self):
        # 新建菜单(可新建 文件/文件夹/xml文件)
        self.new_dialog = New(self, self.project_path)
        self.new_dialog.signal[str].connect(self.get_signal_from_new)
        self.new_dialog.exec()

    # 打开工程文件夹
    def connect_open_folder(self):
        dir_choose = QFileDialog.getExistingDirectory(self, '选取文件夹', self.project_path,
                                                      options=QFileDialog.DontUseNativeDialog)
        if dir_choose:
            self.project_path = Param.project_path = dir_choose
            self.cf.set('default', 'project_path', self.project_path)
            with open(Param.config_file, 'w', encoding='utf-8') as f:
                self.cf.write(f)
            self.project_bar.reload_model(dir_choose)

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

    # 撤销上一次操作
    def connect_undo(self):
        print('撤销上一次操作')

    def connect_redo(self):
        print('恢复上一次操作')

    def connect_cut(self):
        print('剪切')

    def connect_copy(self):
        print('复制')

    def connect_paste(self):
        print('粘贴')

    def connect_delete(self):
        print('删除')

    def connect_select_all(self):
        print('全选')

    def connect_comment(self):
        print('注释')

    def connect_search(self):
        print('检索')

    def connect_replace(self):
        print('替换')

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
            reply = QMessageBox.question(self, '有文件未保存', file+'未保存\n是否先保存文件？',
                                         QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.No)
            if reply == QMessageBox.No:
                event.accept()
            elif reply == QMessageBox.Cancel:
                event.ignore()
            elif reply == QMessageBox.Yes:
                self.editor_widget.save_edit_tab(file)
                event.accept()
            else:
                event.ignore()


if __name__ == '__main__':
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
