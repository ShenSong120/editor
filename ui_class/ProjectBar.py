import os
import time
import shutil
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from threading import Thread
from glv import MergePath
from ui_class.FileTreeView import FileTreeView


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
        filters = ['*']
        self.model.setRootPath(self.path)
        self.model.setNameFilters(filters)
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
        self.new_file_action = QAction('新建文件', self)
        self.new_file_action.setShortcut('ctrl+n')
        self.new_file_action.triggered.connect(self.new_file_dialog)
        # 新建文件夹
        self.new_folder_action = QAction('新建文件夹', self)
        self.new_folder_action.setShortcut('ctrl+shift+n')
        self.new_folder_action.triggered.connect(self.new_folder_dialog)
        # 重命名
        self.rename_action = QAction('重命名', self)
        self.rename_action.setShortcut('f2')
        self.rename_action.triggered.connect(self.rename_dialog)
        # 删除
        self.delete_action = QAction('删除', self)
        self.delete_action.setShortcut('delete')
        self.delete_action.triggered.connect(self.delete_dialog)
        # 菜单添加action
        self.menu.addAction(self.copy_action)
        self.menu.addAction(self.paste_action)
        self.menu.addAction(self.copy_path_action)
        self.menu.addAction(self.new_file_action)
        self.menu.addAction(self.new_folder_action)
        self.menu.addAction(self.rename_action)
        self.menu.addAction(self.delete_action)
        self.menu.exec(self.tree.mapToGlobal(point))

    # 复制文件
    def copy(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.node_path)
        print(self.node_path)

    # 粘贴文件
    def paste(self):
        clipboard = QApplication.clipboard()
        copy_path = clipboard.text()
        title, prompt_text, default_name = '新建文件', '请输入文件名', os.path.split(copy_path)[1]
        file_name, ok = QInputDialog.getText(self, title, prompt_text, QLineEdit.Normal, default_name)
        if ok:
            if os.path.isdir(self.node_path) is True:
                root_path = self.node_path
                if self.index is not None:
                    # 展开文件夹
                    self.tree.setExpanded(self.index, True)
            else:
                root_path = os.path.dirname(self.node_path)
            paste_path = MergePath(root_path, file_name).merged_path
            shutil.copy(copy_path, paste_path)
            Thread(target=self.update_select_item, args=(paste_path,)).start()
            print(paste_path)

    # 复制路径
    def copy_path(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.node_path)

    # 新建文件
    def new_file_dialog(self):
        title, prompt_text, default_name = '新建文件', '请输入文件名', 'new.xml'
        file_name, ok = QInputDialog.getText(self, title, prompt_text, QLineEdit.Normal, default_name)
        if ok:
            if os.path.isdir(self.node_path) is True:
                root_path = self.node_path
                if self.index is not None:
                    # 展开文件夹
                    self.tree.setExpanded(self.index, True)
            else:
                root_path = os.path.dirname(self.node_path)
            file_path = MergePath(root_path, file_name).merged_path
            # 如果文件存在
            if os.path.exists(file_path):
                reply = QMessageBox.question(self, '新建此文件已经存在', '是否替换已经存在的文件？', QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.No)
                if reply == QMessageBox.No:
                    self.new_file_dialog()
                elif reply == QMessageBox.Yes:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        text = "<?xml version='1.0' encoding='utf-8' ?>"
                        f.write(text)
                        print('新建文件: %s' % file_path)
                    # 更新选中item
                    Thread(target=self.update_select_item, args=(file_path,)).start()
                    self.signal.emit('new_xml>' + str(file_path))
                elif reply == QMessageBox.Cancel:
                    pass
            else:
                with open(file_path, 'w', encoding='utf-8') as f:
                    text = "<?xml version='1.0' encoding='utf-8' ?>"
                    f.write(text)
                    print('新建文件: %s' % file_path)
                # 更新选中item
                Thread(target=self.update_select_item, args=(file_path,)).start()
                self.signal.emit('new_xml>' + str(file_path))

    # 新建文件夹
    def new_folder_dialog(self):
        title, prompt_text, default_name = '新建文件夹', '请输入文件夹名', ''
        folder_name, ok = QInputDialog.getText(self, title, prompt_text, QLineEdit.Normal, default_name)
        if ok:
            if os.path.isdir(self.node_path) is True:
                root_path = self.node_path
                if self.index is not None:
                    # 展开文件夹
                    self.tree.setExpanded(self.index, True)
            else:
                root_path = os.path.dirname(self.node_path)
            folder_path = MergePath(root_path, folder_name).merged_path
            # 如果目录存在
            if os.path.exists(folder_path):
                reply = QMessageBox.question(self, '新建此目录已经存在', '是否将新建目录和已存在目录合并？', QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.No)
                if reply == QMessageBox.No:
                    self.new_folder_dialog()
                elif reply == QMessageBox.Yes:
                    pass
                elif reply == QMessageBox.Cancel:
                    pass
            else:
                os.makedirs(folder_path)
                print('新建文件夹: %s' % folder_path)
                # 更新选中item
                Thread(target=self.update_select_item, args=(folder_path,)).start()

    # 重命名
    def rename_dialog(self):
        if self.blank_click_flag is True:
            return
        title, prompt_text, default_name = '重命名', '请输入新文件名', self.node_name
        new_name, ok = QInputDialog.getText(self, title, prompt_text, QLineEdit.Normal, default_name)
        if ok:
            root_path = os.path.dirname(self.node_path)
            new_name_path = MergePath(root_path, new_name).merged_path
            # 如果新命名文件存在
            if os.path.exists(new_name_path):
                reply = QMessageBox.question(self, '新命名文件已经存在', '是否替换已经存在的文件？', QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.No)
                if reply == QMessageBox.No:
                    self.rename_dialog()
                elif reply == QMessageBox.Yes:
                    os.rename(self.node_path, new_name_path)
                    print('重命名 %s 为: %s' % (self.node_path, new_name_path))
                    Thread(target=self.update_select_item, args=(new_name_path,)).start()
                elif reply == QMessageBox.Cancel:
                    pass
            else:
                os.rename(self.node_path, new_name_path)
                print('重命名 %s 为: %s' % (self.node_path, new_name_path))
                Thread(target=self.update_select_item, args=(new_name_path,)).start()


    # 删除文件
    def delete_dialog(self):
        if self.blank_click_flag is True:
            return
        # file_flag判断是文件还是文件夹(文件为True,文件夹为False)
        if os.path.isdir(self.node_path) is True:
            file_flag = False
            prompt_text = '确定要删除此文件夹吗？'
        else:
            file_flag = True
            prompt_text = '确定要删除此文件吗？'
        # 判断是否确定删除
        reply = QMessageBox.question(self, '删除栏', prompt_text, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            # 获取删除项下一项名字
            name = self.tree.indexBelow(self.model.index(self.node_path)).data()
            parent_path = os.path.split(self.node_path)[0]
            # 确保路径存在
            selected_path = parent_path if name is None else MergePath(parent_path, name).merged_path
            if os.path.exists(selected_path) is False:
                selected_path = parent_path
            Thread(target=self.update_select_item, args=(selected_path,)).start()
            self.info_label.setText(selected_path)
            if file_flag is True:
                os.remove(self.node_path)
                print('删除文件: %s' % self.node_path)
                self.signal.emit('delete>' + self.node_path)
            else:
                shutil.rmtree(self.node_path)
                print('删除文件夹: %s' % self.node_path)

    # 更新选中item(必须异步线程才能选中, 也就是等待文件model更新完成, 延时时间不能太短)
    def update_select_item(self, path):
        time.sleep(0.04)
        new_index = self.model.index(path)
        self.tree.setCurrentIndex(new_index)
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
                self.blank_click_flag = False
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
                self.blank_click_flag = False
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
                print('暂不支持打开此类型文件!!!')
        else:
            pass

    # 工具栏快捷键
    def keyPressEvent(self, event):
        # Ctrl + C 复制
        if (event.key() == Qt.Key_C):
            if event.modifiers() == Qt.ControlModifier:
                self.copy()
                print('复制')
            else:
                QWidget.keyPressEvent(self, event)
        # Ctrl + V 粘贴
        if (event.key() == Qt.Key_V):
            if event.modifiers() == Qt.ControlModifier:
                self.paste()
                print('粘贴')
            else:
                QWidget.keyPressEvent(self, event)
        # Ctrl + Shift + C 复制路径
        if (event.key() == Qt.Key_C):
            if event.modifiers() == Qt.ControlModifier | Qt.ShiftModifier:
                self.copy_path()
                print('复制路径')
            else:
                QWidget.keyPressEvent(self, event)
        # Ctrl + N 新建文件
        if (event.key() == Qt.Key_N):
            if event.modifiers() == Qt.ControlModifier:
                self.new_file_dialog()
                print('新建文件')
            else:
                QWidget.keyPressEvent(self, event)
        # Ctrl + Shift + N 新建文件夹
        if (event.key() == Qt.Key_N):
            if event.modifiers() == Qt.ControlModifier | Qt.ShiftModifier:
                self.new_folder_dialog()
                print('新建文件夹')
            else:
                QWidget.keyPressEvent(self, event)
        # Shift + F2 重命名
        if (event.key() == Qt.Key_F2):
            if event.modifiers() == Qt.ShiftModifier:
                self.rename_dialog()
                print('重命名')
            else:
                QWidget.keyPressEvent(self, event)
        # Delete 删除
        if (event.key() == Qt.Key_Delete):
            self.delete_dialog()
            print('删除')
        # 其余情况
        else:
            QWidget.keyPressEvent(self, event)