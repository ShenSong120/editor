import os
import time
import shutil
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from threading import Thread
from glv import MergePath
from ui_class.FileTreeView import FileTreeView
from ui_class.FileDialog import Paste, NewFolder, NewFile, Rename, Delete
from ui_class.New import New


# 侧边工程栏
class ProjectBar(QWidget):

    signal = pyqtSignal(str)

    def __init__(self, parent, path):
        super(ProjectBar, self).__init__(parent)
        # 设置工程栏背景颜色
        self.setStyleSheet('background-color: #F0F0F0;')
        self.parent = parent
        self.path = path
        # 文件树状态标志(初始为None)
        self.node_path = self.path
        self.node_name = 'new.xml'
        self.index = None
        self.blank_click_flag = True
        # 文件模型
        self.model = QFileSystemModel(self)
        # 改表头名字(无效)
        # self.model.setHeaderData(0, Qt.Horizontal, "123455")
        # 文件过滤
        # self.model.setFilter(QDir.NoDotAndDotDot | QDir.AllDirs)
        # 需要显示的文件
        # filters = ['*.mp4', '*.avi', '*.mov', '*.flv', '*.html', '*.jpg', '*.png', '*.xls', '*.xlsx', '*.xml', '*.txt', '*.ini']
        self.filters = ['*']
        self.model.setRootPath(self.path)
        self.model.setNameFilters(self.filters)
        self.model.setNameFilterDisables(False)
        # 树形视图
        # self.tree = QTreeView(self)
        self.tree = FileTreeView(self)
        self.tree.signal[str].connect(self.get_signal_from_file_tree)
        # 右键菜单
        self.tree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree.customContextMenuRequested.connect(self.show_menu)
        self.tree.setModel(self.model)
        # 后面的size/type/data不显示
        self.tree.setColumnHidden(1, True)
        self.tree.setColumnHidden(2, True)
        self.tree.setColumnHidden(3, True)
        self.tree.setHeaderHidden(True)
        self.tree.setRootIndex(self.model.index(self.path))
        # self.tree.doubleClicked.connect(lambda : self.operation_file(None))
        # 工程栏路径信息展示
        self.info_label = QLineEdit(self)
        self.info_label.setReadOnly(True)
        self.info_label.setText(self.path)
        # 总体布局
        self.v_layout = QVBoxLayout()
        self.v_layout.setContentsMargins(0, 0, 0, 0)
        self.v_layout.setSpacing(0)
        self.v_layout.addWidget(self.info_label)
        self.v_layout.addWidget(self.tree)
        self.setLayout(self.v_layout)

    # 重新载入目录树
    def reload_model(self, path):
        self.path = path
        filters = ['*']
        self.model.setRootPath(self.path)
        self.model.setNameFilters(filters)
        self.model.setNameFilterDisables(False)
        self.model.setRootPath(self.path)
        self.model.setNameFilters(self.filters)
        self.model.setNameFilterDisables(False)
        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index(self.path))
        self.info_label.setText(self.path)
        # 文件树状态标志(初始为None)
        self.node_path = self.path
        self.node_name = 'new.xml'
        self.index = None
        self.blank_click_flag = True

    def show_menu(self, point):
        self.index = self.tree.indexAt(point)
        # 如果点击的非空白区域
        if self.index.isValid():
            # 当前节点路径以及名字
            # index = self.tree.currentIndex()
            self.node_name = self.model.fileName(self.index)
            self.node_path = self.model.filePath(self.index)
            self.blank_click_flag = False
        # 点击空白区域
        else:
            self.tree.clearSelection()
            self.node_name = os.path.split(self.path)[1]
            self.node_path = self.path
            self.blank_click_flag = True
        # 更新显示标签
        self.info_label.setText(self.node_path)
        # 菜单样式
        menu_qss = "QMenu{color: #E8E8E8; background: #4D4D4D; margin: 2px;}\
                    QMenu::item{padding:3px 20px 3px 20px;}\
                    QMenu::indicator{width:13px; height:13px;}\
                    QMenu::item:selected:enabled{color:#E8E8E8; border:0px solid #575757; background:#1E90FF;}\
                    QMenu::item:selected:!enabled{color:#969696; border:0px solid #575757; background:#99CCFF;}\
                    QMenu::item:!enabled{color:#969696;}\
                    QMenu::item: enabled{color:#242424;}\
                    QMenu::separator{height:1px; background:#757575;}"

        self.menu = QMenu(self)
        self.menu.setStyleSheet(menu_qss)
        # 复制
        self.copy_action = QAction('复制', self)
        self.copy_action.setShortcut('ctrl+c')
        self.copy_action.triggered.connect(self.copy)
        # 粘贴
        self.paste_action = QAction('粘贴', self)
        self.paste_action.setShortcut('ctrl+v')
        self.paste_action.triggered.connect(self.paste)
        # 复制路径
        self.copy_path_action = QAction('复制路径', self)
        self.copy_path_action.setShortcut('ctrl+shift+c')
        self.copy_path_action.triggered.connect(self.copy_path)
        # 新建文件
        self.new_action = QAction('新建', self)
        self.new_action.setShortcut('ctrl+n')
        self.new_action.triggered.connect(self.new)
        # 重命名
        self.rename_action = QAction('重命名', self)
        self.rename_action.setShortcut('f2')
        self.rename_action.triggered.connect(self.rename)
        # 删除
        self.delete_action = QAction('删除', self)
        self.delete_action.setShortcut('delete')
        self.delete_action.triggered.connect(self.delete)
        # 设置action使能
        if self.blank_click_flag is True:
            self.copy_action.setEnabled(False)
            self.copy_path_action.setEnabled(False)
            self.rename_action.setEnabled(False)
            self.delete_action.setEnabled(False)
        # 菜单添加action
        self.menu.addAction(self.copy_action)
        self.menu.addAction(self.paste_action)
        self.menu.addAction(self.copy_path_action)
        self.menu.addAction(self.new_action)
        self.menu.addAction(self.rename_action)
        self.menu.addAction(self.delete_action)
        self.menu.exec(self.tree.mapToGlobal(point))

    # 新建(可以选择文件/文件夹等)
    def new(self):
        # 新建菜单(可新建 文件/文件夹/xml文件)
        self.new_dialog = New(self, self.node_path)
        self.new_dialog.signal[str].connect(self.get_signal_from_file_dialog)
        self.new_dialog.exec()

    # 复制文件
    def copy(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.node_path)

    # 粘贴文件
    def paste(self):
        clipboard = QApplication.clipboard()
        copy_path = clipboard.text()
        if os.path.isdir(self.node_path):
            start_path = self.node_path
        else:
            start_path = os.path.dirname(self.node_path)
        self.paste_dialog = Paste(self, copy_path, start_path)
        self.paste_dialog.signal[str].connect(self.get_signal_from_file_dialog)
        self.paste_dialog.exec()

    # 复制路径
    def copy_path(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.node_path)

    # 重命名
    def rename(self):
        if self.blank_click_flag is True:
            return
        self.rename_dialog = Rename(self, self.node_path)
        self.rename_dialog.signal[str].connect(self.get_signal_from_file_dialog)
        self.rename_dialog.exec()

    # 删除文件
    def delete(self):
        if self.blank_click_flag is True:
            return
        self.delete_dialog = Delete(self, self.node_path)
        self.delete_dialog.signal[str].connect(self.get_signal_from_file_dialog)
        self.delete_dialog.exec()

    # 从文件窗口接收消息
    def get_signal_from_file_dialog(self, signal_str):
        flag = signal_str.split('>')[0]
        path = signal_str.split('>')[1]
        if os.path.exists(path):
            self.update_select_item(path)
            self.operation_file(path)
        else:
            # 路径不存在就是删除标志(需要删掉子tab)
            self.signal.emit('delete_path>' + path)

    # 更新选中item(也就是等待文件model更新完成, 延时时间不能太短)
    def update_select_item(self, path):
        self.reload_model(self.path)
        time.sleep(0.04)
        self.node_path = path
        self.node_name = os.path.split(path)[1]
        self.index = self.model.index(path)
        self.blank_click_flag = False
        self.tree.setCurrentIndex(self.index)
        self.info_label.setText(path)

    # 获取从文件树获取到的信号
    def get_signal_from_file_tree(self, signal_str):
        flag = signal_str.split('>')[0]
        signal = eval(signal_str.split('>')[1])
        # 接受到的point信息
        if flag == 'click_point':
            point = QPoint(signal[0], signal[1])
            self.index = self.tree.indexAt(point)
            if self.index.isValid():
                self.node_name = self.model.fileName(self.index)
                self.node_path = self.model.filePath(self.index)
                self.blank_click_flag = False
            else:
                self.tree.clearSelection()
                self.node_name = os.path.split(self.path)[1]
                self.node_path = self.path
                self.blank_click_flag = True
        elif flag == 'double_click_point':
            point = QPoint(signal[0], signal[1])
            self.index = self.tree.indexAt(point)
            if self.index.isValid():
                self.node_name = self.model.fileName(self.index)
                self.node_path = self.model.filePath(self.index)
                self.blank_click_flag = False
                self.operation_file()
            else:
                self.tree.clearSelection()
                self.node_name = os.path.split(self.path)[1]
                self.node_path = self.path
                self.blank_click_flag = True
        # 更新显示标签
        self.info_label.setText(self.node_path)

    # 双击操作
    def operation_file(self, file_path=None):
        if file_path is None:
            index = self.tree.currentIndex()
            file_path = self.model.filePath(index)
        else:
            file_path = file_path
        # 判断双击是否为文件(只对文件操作)
        if os.path.isfile(file_path) is True:
            # 打开xml文件
            if file_path.endswith('.xml') or file_path.endswith('.XML'):
                self.signal.emit('open_xml>' + str(file_path))
            else:
                pass
        else:
            pass

    # 工具栏快捷键
    def keyPressEvent(self, event):
        # Ctrl + C 复制
        if (event.key() == Qt.Key_C):
            if event.modifiers() == Qt.ControlModifier:
                if self.blank_click_flag is False:
                    self.copy()
            else:
                QWidget.keyPressEvent(self, event)
        # Ctrl + V 粘贴
        if (event.key() == Qt.Key_V):
            if event.modifiers() == Qt.ControlModifier:
                self.paste()
            else:
                QWidget.keyPressEvent(self, event)
        # Ctrl + Shift + C 复制路径
        if (event.key() == Qt.Key_C):
            if event.modifiers() == Qt.ControlModifier | Qt.ShiftModifier:
                if self.blank_click_flag is False:
                    self.copy_path()
            else:
                QWidget.keyPressEvent(self, event)
        # Ctrl + N 新建文件、文件夹等等
        if (event.key() == Qt.Key_N):
            if event.modifiers() == Qt.ControlModifier:
                self.new()
            else:
                QWidget.keyPressEvent(self, event)
        # Shift + F2 重命名
        if (event.key() == Qt.Key_F2):
            if event.modifiers() == Qt.ShiftModifier:
                if self.blank_click_flag is False:
                    self.rename()
            else:
                QWidget.keyPressEvent(self, event)
        # Delete 删除
        if (event.key() == Qt.Key_Delete):
            if self.blank_click_flag is False:
                self.delete()
        # 其余情况
        else:
            QWidget.keyPressEvent(self, event)