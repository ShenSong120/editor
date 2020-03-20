# coding:utf-8
import os
import sys
import json
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from other.glv import Icon, Param, MergePath, BeautifyStyle, EditorAction, View
from ui_class.ProjectBar import ProjectBar
from ui_class.EditorTab import EditorTab
from ui_class.New import New
from ui_class.TreeStructure import TreeStructure
from ui_class.SettingDialog import Setting
from other.CaseConfigParser import CaseConfigParser


# 编辑器窗口app
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
        # 结构树
        self.structure_tree = TreeStructure(self.central_widget)
        # 全局竖直布局
        self.general_v_layout = QVBoxLayout(self.central_widget)
        self.general_v_layout.setContentsMargins(1, 0, 0, 0)
        # 分割窗口布局
        self.splitter_h_general = QSplitter(Qt.Horizontal)
        self.splitter_h_general.setHandleWidth(0)
        self.splitter_h_general.addWidget(self.project_bar)
        self.splitter_h_general.addWidget(self.editor_widget)

        self.splitter_h_general.addWidget(self.structure_tree)

        # 按比例分割
        # self.splitter_h_general.setStretchFactor(0, 1)
        # self.splitter_h_general.setStretchFactor(1, 4)
        # 按尺寸分割
        self.splitter_h_general.setSizes([150, 800, 150])
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
        # 视图动作
        self.mini_map_switch_action = QAction(QIcon(Icon.mini_map), '小地图', self)
        self.mini_map_switch_action.triggered.connect(self.connect_mini_map_switch)
        self.structure_show_switch_action = QAction(QIcon(Icon.structure), '结构', self)
        self.structure_show_switch_action.triggered.connect(self.connect_structure_show)
        # 设置动作
        self.setting_action = QAction(QIcon(Icon.setting), '设置', self)
        self.setting_action.triggered.connect(self.connect_setting)
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
        # 视图菜单栏
        self.view_menu_bar = self.menu_bar.addMenu('视图')
        self.view_menu_bar.addAction(self.mini_map_switch_action)
        self.view_menu_bar.addAction(self.structure_show_switch_action)
        # 设置菜单栏
        self.setting_menu_bar = self.menu_bar.addMenu('设置')
        self.setting_menu_bar.addAction(self.setting_action)
        # 帮助菜单栏
        self.help_menu_bar = self.menu_bar.addMenu('帮助')
        self.help_action = QAction('操作说明', self)
        self.help_action.triggered.connect(self.connect_help)
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
        # 视图工具栏
        self.view_tool_bar = self.addToolBar('view_tool_bar')
        self.view_tool_bar.setMaximumHeight(32)
        self.view_tool_bar.addAction(self.mini_map_switch_action)
        self.view_tool_bar.addAction(self.structure_show_switch_action)
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
        self.cursor_icon = QToolButton(self)
        self.cursor_icon.setStyleSheet('QToolButton{border-image: url(' + Icon.cursor + ')}')
        self.cursor_label = QLabel(self)
        self.cursor_label.setText('')
        # 状态栏布局
        self.status_bar.addPermanentWidget(self.file_icon, stretch=0)
        self.status_bar.addPermanentWidget(self.file_path_label, stretch=1)
        self.status_bar.addPermanentWidget(self.cursor_icon, stretch=0)
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
        # 函数跳转
        elif flag == 'dump_in_function':
            file_path = signal_str.split('>')[1]
            self.editor_widget.open_edit_tab(file_path)
        # 更新工具栏动作状态
        elif flag == 'action':
            self.update_tool_bar_enable_status(signal_str.split('>')[1])
        # 关闭子tab
        elif flag == 'remove_tab':
            file_path = signal_str.split('>')[1]
            index = [tree.file for tree in self.structure_tree.tree_list].index(file_path)
            self.structure_tree.tree_list.pop(index)
        # 关闭所有子tab信号
        elif flag == 'close_all_tab':
            self.set_edit_tool_bar_enable(status=False)
            # 关闭tree
            self.structure_tree.close_tree()
        # 更新树
        elif flag == 'update_tree':
            file_path = signal_str.split('>')[1]
            self.structure_tree.update_tree(file_path)
        else:
            pass

    # 获取工程栏发出的信号
    def get_signal_from_project_bar(self, signal_str):
        flag = signal_str.split('>')[0]
        path = signal_str.split('>')[1]
        # 打开文件
        if flag == 'open_xml':
            self.editor_widget.open_edit_tab(path)
        # 重命名文件
        elif flag == 'rename_path':
            old_path = path.split('==')[0]
            new_path = path.split('==')[1]
            if old_path in self.editor_widget.file_list:
                index = self.editor_widget.file_list.index(old_path)
                tab_name = os.path.split(new_path)[1]
                self.editor_widget.file_list[index] = new_path
                self.editor_widget.setTabText(index, tab_name)
                self.editor_widget.setTabToolTip(index, new_path)
                index = [tree.file for tree in self.structure_tree.tree_list].index(old_path)
                self.structure_tree.tree_list[index].file = old_path
                self.structure_tree.tree_list[index].root.setText(0, tab_name)
        # 删除
        elif flag == 'delete_path':
            if path in self.editor_widget.file_list:
                index = self.editor_widget.file_list.index(path)
                self.close_tab(index)
                index = [tree.file for tree in self.structure_tree.tree_list].index(path)
                self.structure_tree.tree_list.pop(index)
        # 粘贴
        elif flag == 'paste_path':
            pass
        # 新建文件
        elif flag == 'new_file':
            pass
        # 新建文件夹
        elif flag == 'new_folder':
            pass

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
        pass
        # 改为自动保存
        # self.editor_widget.save_edit_tab()

    # 另存文件为
    def connect_save_as_file(self):
        self.editor_widget.save_file_as_tab()

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

    # 获取当前编辑器
    def get_current_editor(self):
        editor = self.editor_widget.currentWidget()
        return editor

    # 撤销上一次操作
    def connect_undo(self):
        editor = self.get_current_editor()
        editor.undo()

    # 恢复上一次操作
    def connect_redo(self):
        editor = self.get_current_editor()
        editor.redo()

    # 剪切
    def connect_cut(self):
        editor = self.get_current_editor()
        editor.cut()

    # 复制
    def connect_copy(self):
        editor = self.get_current_editor()
        editor.copy()

    # 粘贴
    def connect_paste(self):
        editor = self.get_current_editor()
        editor.paste()

    # 删除
    def connect_delete(self):
        editor = self.get_current_editor()
        editor.delete()

    # 选取所有
    def connect_select_all(self):
        editor = self.get_current_editor()
        editor.select_all()

    # 注释
    def connect_comment(self):
        editor = self.get_current_editor()
        editor.comment()

    # 搜索
    def connect_search(self):
        editor = self.get_current_editor()
        editor.search()

    # 替换
    def connect_replace(self):
        editor = self.get_current_editor()
        editor.replace()

    def connect_help(self):
        pass

    # mini_map开关
    def connect_mini_map_switch(self):
        tab_counts = self.editor_widget.count()
        if tab_counts > 0:
            View.mini_map_switch = bool(1 - View.mini_map_switch)
            for i in range(tab_counts):
                editor = self.editor_widget.widget(i)
                if View.mini_map_switch is True:
                    editor.mini_map.setHidden(False)
                else:
                    editor.mini_map.setHidden(True)

    # structure_tree开关
    def connect_structure_show(self):
        if self.structure_tree.isHidden():
            self.structure_tree.setHidden(False)
        else:
            self.structure_tree.setHidden(True)

    # 设置动作
    def connect_setting(self):
        setting_dialog = Setting(None)
        setting_dialog.exec()

    # 窗口关闭事件
    def closeEvent(self, event):
        event.accept()


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
