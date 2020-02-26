import os
import shutil
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from other.glv import Icon, MergePath, BeautifyStyle


class NewFile(QDialog):

    signal = pyqtSignal(str)

    def __init__(self, parent, path, type=None):
        super(NewFile, self).__init__(parent)
        # 文件类型
        self.file_type = type
        # 文件首行(例如xml行首需要有文件标志)
        self.file_text = self.get_file_first_row_text(self.file_type)
        # 文件默认名
        self.default_name = self.get_file_default_name(self.file_type)
        # 文件窗口标题
        self.window_title = '新建文件'
        if type is not None:
            self.window_title = '新建' + type + '文件'
        # 新建文件起始路径
        if os.path.isdir(path):
            self.start_path = path
        else:
            self.start_path = os.path.dirname(path)
        self.title = QLabel(self)
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setText(self.window_title)
        self.h_line = QFrame(self)
        self.h_line.setFrameShape(QFrame.HLine)
        self.title_layout = QVBoxLayout()
        self.title_layout.addWidget(self.title)
        self.title_layout.addWidget(self.h_line)
        # 文件路径选择以及文件名字输入
        self.path_text = QLineEdit(self)
        self.path_text.setReadOnly(True)
        self.path_text.setText(self.start_path)
        self.select_path_action = QAction(self.path_text)
        self.select_path_action.setIcon(QIcon(Icon.path))
        self.select_path_action.triggered.connect(self.select_path)
        self.path_text.addAction(self.select_path_action, QLineEdit.TrailingPosition)
        self.file_name_text = QLineEdit(self)
        self.file_name_text.setPlaceholderText(self.default_name)
        self.form_layout = QFormLayout()
        self.form_layout.setSpacing(20)
        self.form_layout.addRow('文件路径:', self.path_text)
        self.form_layout.addRow('文件名字:', self.file_name_text)
        # 确定和取消按钮
        self.sure_button = QPushButton('确定', self)
        self.sure_button.clicked.connect(self.click_sure)
        self.sure_button.setFixedWidth(100)
        self.cancel_button = QPushButton('取消', self)
        self.cancel_button.clicked.connect(self.click_cancel)
        self.cancel_button.setFixedWidth(100)
        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.sure_button)
        self.button_layout.addWidget(self.cancel_button)
        # 全局布局
        self.general_layout = QVBoxLayout(self)
        self.general_layout.setContentsMargins(0, 5, 0, 5)
        self.general_layout.addLayout(self.title_layout)
        self.general_layout.addSpacing(20)
        self.general_layout.addLayout(self.form_layout)
        self.general_layout.addSpacing(20)
        self.general_layout.addLayout(self.button_layout)
        self.setLayout(self.general_layout)
        self.setMinimumWidth(600)
        # self.setWindowTitle('')

    # 获取文件首行(如)
    def get_file_first_row_text(self, type):
        if type in ['xml', 'XML']:
            first_row_text = '<?xml version="1.0" encoding="utf-8" ?>'
        else:
            first_row_text = ''
        return first_row_text

    # 获取文件默认名(如)
    def get_file_default_name(self, type):
        if type in ['xml', 'XML']:
            default_name = 'new.xml'
        else:
            default_name = 'new.xxx'
        return default_name

    def select_path(self):
        dir_choose = QFileDialog.getExistingDirectory(self, '选取文件夹', self.start_path, options=QFileDialog.DontUseNativeDialog)
        if dir_choose:
            self.path_text.setText(dir_choose)

    def click_sure(self):
        self.setHidden(True)
        file_name = self.file_name_text.text()
        if file_name == '':
            file_name = self.default_name
        if self.file_type is None:
            if '.' not in file_name:
                # 发出后缀警告
                QMessageBox.warning(self,'消息框标题', '文件名后缀错误！\n请重新输入文件名',
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
                self.setHidden(False)
                return
            else:
                file_name = file_name
                self.file_text = self.get_file_first_row_text(file_name.split('.')[1])
        # 声明了文件类型
        else:
            if '.' not in file_name:
                file_name = file_name + '.' + self.file_type
            else:
                file_name = file_name
        file_path = MergePath(self.path_text.text(), file_name).merged_path
        if os.path.exists(file_path):
            self.deal_existed_file(file_path)
        else:
            self.deal_not_existed_file(file_path)

    def click_cancel(self):
        self.setHidden(True)

    # 处理已经存在的文件(需要先添加警告)
    def deal_existed_file(self, file):
        reply = QMessageBox.question(self, '新建此文件已经存在', '是否替换已经存在的文件？',
                                     QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.No)
        if reply == QMessageBox.No:
            self.setHidden(False)
        elif reply == QMessageBox.Yes:
            with open(file, 'w', encoding='utf-8') as f:
                f.write(self.file_text)
            # 发射文件新建信号
            self.signal.emit('new_file>' + file)
        else:
            pass

    def deal_not_existed_file(self, file):
        with open(file, 'w', encoding='utf-8') as f:
            f.write(self.file_text)
        # 发射文件新建信号
        self.signal.emit('new_file>' + file)


class NewFolder(QDialog):

    signal = pyqtSignal(str)

    def __init__(self, parent, path):
        super(NewFolder, self).__init__(parent)
        # 新建文件夹起始路径
        self.start_path = path
        # 默认文件夹名
        self.default_name = 'new-folder'
        self.title = QLabel(self)
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setText('新建文件夹')
        self.h_line = QFrame(self)
        self.h_line.setFrameShape(QFrame.HLine)
        self.title_layout = QVBoxLayout()
        self.title_layout.addWidget(self.title)
        self.title_layout.addWidget(self.h_line)
        # 文件路径选择以及文件夹名字输入
        self.path_text = QLineEdit(self)
        self.path_text.setReadOnly(True)
        self.path_text.setText(self.start_path)
        self.select_path_action = QAction(self.path_text)
        self.select_path_action.setIcon(QIcon(Icon.path))
        self.select_path_action.triggered.connect(self.select_path)
        self.path_text.addAction(self.select_path_action, QLineEdit.TrailingPosition)
        self.folder_name_text = QLineEdit(self)
        self.folder_name_text.setPlaceholderText(self.default_name)
        self.form_layout = QFormLayout()
        self.form_layout.setSpacing(20)
        self.form_layout.addRow('文件夹路径:', self.path_text)
        self.form_layout.addRow('文件夹名字:', self.folder_name_text)
        # 确定和取消按钮
        self.sure_button = QPushButton('确定', self)
        self.sure_button.clicked.connect(self.click_sure)
        self.sure_button.setFixedWidth(100)
        self.cancel_button = QPushButton('取消', self)
        self.cancel_button.clicked.connect(self.click_cancel)
        self.cancel_button.setFixedWidth(100)
        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.sure_button)
        self.button_layout.addWidget(self.cancel_button)
        # 全局布局
        self.general_layout = QVBoxLayout(self)
        self.general_layout.setContentsMargins(0, 5, 0, 5)
        self.general_layout.addLayout(self.title_layout)
        self.general_layout.addSpacing(20)
        self.general_layout.addLayout(self.form_layout)
        self.general_layout.addSpacing(20)
        self.general_layout.addLayout(self.button_layout)
        self.setLayout(self.general_layout)
        self.setMinimumWidth(600)

    def select_path(self):
        dir_choose = QFileDialog.getExistingDirectory(self, '选取文件夹', self.start_path, options=QFileDialog.DontUseNativeDialog)
        if dir_choose:
            self.path_text.setText(dir_choose)

    def click_sure(self):
        self.setHidden(True)
        folder_name = self.folder_name_text.text()
        if folder_name == '':
            folder_name = self.default_name
        folder_path = MergePath(self.path_text.text(), folder_name).merged_path
        if os.path.exists(folder_path):
            self.deal_existed_folder(folder_path)
        else:
            self.deal_not_existed_folder(folder_path)

    def click_cancel(self):
        self.setHidden(True)

    # 处理已经存在的文件夹(需要先添加警告)
    def deal_existed_folder(self, folder):
        reply = QMessageBox.question(self, '新建此文件夹已经存在', '是否将此文件夹和已经存在的文件夹合并？',
                                     QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.No)
        if reply == QMessageBox.No:
            self.setHidden(False)
        elif reply == QMessageBox.Yes:
            # 发射文件夹新建信号
            self.signal.emit('new_folder>' + folder)
        else:
            pass

    def deal_not_existed_folder(self, folder):
        os.makedirs(folder)
        # 发射文件夹新建信号
        self.signal.emit('new_folder>' + folder)


# 粘贴文件
class Paste(QDialog):

    signal = pyqtSignal(str)

    def __init__(self, parent, path_list, start_path):
        super(Paste, self).__init__(parent)
        # 需要粘贴的路径列表
        self.path_list = path_list
        # 文件系统起始路径
        self.start_path = start_path
        # 自定义控件title
        self.title = QLabel(self)
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setText('粘贴')
        self.h_line = QFrame(self)
        self.h_line.setFrameShape(QFrame.HLine)
        self.title_layout = QVBoxLayout()
        self.title_layout.addWidget(self.title)
        self.title_layout.addWidget(self.h_line)
        # 路径选择以及名字输入
        self.target_path_text = QLineEdit(self)
        self.target_path_text.setReadOnly(True)
        self.target_path_text.setText(self.start_path)
        self.select_path_action = QAction(self.target_path_text)
        self.select_path_action.setIcon(QIcon(Icon.path))
        self.select_path_action.triggered.connect(self.select_path)
        self.target_path_text.addAction(self.select_path_action, QLineEdit.TrailingPosition)
        # 单文件和多文件区别(窗口显示不同)
        if len(self.path_list) == 1:
            # 源文件路径
            source_path = self.path_list[0]
            self.source_path_text = QLineEdit(self)
            self.source_path_text.setReadOnly(True)
            self.source_path_text.setText(source_path)
            self.default_name = os.path.split(source_path)[1]
            self.new_name_text = QLineEdit(self)
            self.new_name_text.setPlaceholderText(self.default_name)
            self.new_name_text.selectAll()
            self.form_layout = QFormLayout()
            self.form_layout.setSpacing(20)
            self.form_layout.addRow('源路径:', self.source_path_text)
            self.form_layout.addRow('目标路径:', self.target_path_text)
            self.form_layout.addRow('目标名字:', self.new_name_text)
        else:
            source_path_list = self.path_list
            self.source_path_text = QLabel(self)
            self.source_path_text.setStyleSheet(BeautifyStyle.label_qss)
            self.source_path_text.setText('\n'.join(source_path_list))
            self.new_name_text = QLabel(self)
            self.form_layout = QFormLayout()
            self.form_layout.setSpacing(20)
            self.form_layout.addRow('源路径:', self.source_path_text)
            self.form_layout.addRow('目标路径:', self.target_path_text)
            self.form_layout.addRow('', self.new_name_text)
        # 确定和取消按钮
        self.sure_button = QPushButton('确定', self)
        self.sure_button.clicked.connect(self.click_sure)
        self.sure_button.setFixedWidth(100)
        self.cancel_button = QPushButton('取消', self)
        self.cancel_button.clicked.connect(self.click_cancel)
        self.cancel_button.setFixedWidth(100)
        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.sure_button)
        self.button_layout.addWidget(self.cancel_button)
        # 全局布局
        self.general_layout = QVBoxLayout(self)
        self.general_layout.setContentsMargins(0, 5, 0, 5)
        self.general_layout.addLayout(self.title_layout)
        self.general_layout.addSpacing(20)
        self.general_layout.addLayout(self.form_layout)
        self.general_layout.addSpacing(20)
        self.general_layout.addLayout(self.button_layout)
        self.setLayout(self.general_layout)
        self.setMinimumWidth(600)

    def select_path(self):
        dir_choose = QFileDialog.getExistingDirectory(self, '选取文件夹', self.start_path, options=QFileDialog.DontUseNativeDialog)
        if dir_choose:
            self.target_path_text.setText(dir_choose)

    def click_sure(self):
        self.setHidden(True)
        # 粘贴的路径为单个路径
        if len(self.path_list) == 1:
            source_path = self.path_list[0]
            target_name = self.new_name_text.text()
            if target_name == '':
                target_name = self.default_name
            target_path = MergePath(self.target_path_text.text(), target_name).merged_path
            if os.path.exists(target_path):
                self.deal_existed_file(source_path, target_path)
            else:
                self.deal_not_existed_file(source_path, target_path)
        # 粘贴的路径为多个路径
        else:
            source_name_list = [os.path.split(path)[1] for path in self.path_list]
            target_path_list = [MergePath(self.target_path_text.text(), name).merged_path for name in source_name_list]
            for i in range(len(self.path_list)):
                source_path = self.path_list[i]
                target_path = target_path_list[i]
                if os.path.exists(target_path):
                    self.deal_existed_file(source_path, target_path)
                else:
                    self.deal_not_existed_file(source_path, target_path)

    def click_cancel(self):
        self.setHidden(True)

    # 处理已经存在的文件(需要先添加警告)
    def deal_existed_file(self, source_path, target_path):
        if os.path.isdir(source_path):
            reply = QMessageBox.question(self, '文件夹重复', source_path+'文件夹已存在\n是否合并这两个已经存在的文件夹？',
                                         QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.No)
            if reply == QMessageBox.No:
                QMessageBox.about(self, '文件夹名重复', source_path+'已存在\n请重新粘贴文件夹并重新命名')
            elif reply == QMessageBox.Yes:
                for name in os.listdir(source_path):
                    if name not in os.listdir(target_path):
                        current_path = MergePath(source_path, name).merged_path
                        if os.path.isdir(current_path):
                            shutil.copytree(current_path, MergePath(target_path, name).merged_path)
                        else:
                            shutil.copyfile(current_path, MergePath(target_path, name).merged_path)
                # 发射粘贴文件夹信号
                self.signal.emit('paste_path>' + target_path)
            else:
                pass
        else:
            reply = QMessageBox.question(self, '文件重复', source_path+'文件已经存在\n是否替换已经存在的文件？',
                                         QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.No)
            if reply == QMessageBox.No:
                QMessageBox.about(self, '文件名重复', source_path+'已存在\n请重新粘贴文件并重新命名')
            elif reply == QMessageBox.Yes:
                if source_path != target_path:
                    shutil.copyfile(source_path, target_path)
                    # 发射粘贴文件信号
                self.signal.emit('paste_path>' + target_path)
            else:
                pass

    def deal_not_existed_file(self, source_path, target_path):
        if os.path.isdir(source_path):
            shutil.copytree(source_path, target_path)
            # 发射粘贴文件夹信号
            self.signal.emit('paste_path>' + target_path)
        else:
            shutil.copyfile(source_path, target_path)
            # 发射粘贴文件信号
            self.signal.emit('paste_path>' + target_path)


# 重命名文件
class Rename(QDialog):

    signal = pyqtSignal(str)

    def __init__(self, parent, source_path):
        super(Rename, self).__init__(parent)
        # 原路径
        self.source_path = source_path
        # 起始路径
        self.start_path = os.path.split(source_path)[0]
        # 默认文件名
        self.default_name = os.path.split(source_path)[1]
        self.title = QLabel(self)
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setText('重命名')
        self.h_line = QFrame(self)
        self.h_line.setFrameShape(QFrame.HLine)
        self.title_layout = QVBoxLayout()
        self.title_layout.addWidget(self.title)
        self.title_layout.addWidget(self.h_line)
        # 源文件路径
        self.source_path_text = QLineEdit(self)
        self.source_path_text.setText(source_path)
        # 重命名文件路径选择以及文件名字输入
        self.rename_path_text = QLineEdit(self)
        self.rename_path_text.setReadOnly(True)
        self.rename_path_text.setText(self.start_path)
        self.select_path_action = QAction(self.rename_path_text)
        self.select_path_action.setIcon(QIcon(Icon.path))
        self.select_path_action.triggered.connect(self.select_path)
        self.rename_path_text.addAction(self.select_path_action, QLineEdit.TrailingPosition)
        self.rename_text = QLineEdit(self)
        self.rename_text.setPlaceholderText(self.default_name)
        self.form_layout = QFormLayout()
        self.form_layout.setSpacing(20)
        self.form_layout.addRow('原路径:', self.source_path_text)
        self.form_layout.addRow('新路径:', self.rename_path_text)
        self.form_layout.addRow('新名字:', self.rename_text)
        # 确定和取消按钮
        self.sure_button = QPushButton('确定', self)
        self.sure_button.clicked.connect(self.click_sure)
        self.sure_button.setFixedWidth(100)
        self.cancel_button = QPushButton('取消', self)
        self.cancel_button.clicked.connect(self.click_cancel)
        self.cancel_button.setFixedWidth(100)
        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.sure_button)
        self.button_layout.addWidget(self.cancel_button)
        # 全局布局
        self.general_layout = QVBoxLayout(self)
        self.general_layout.setContentsMargins(0, 5, 0, 5)
        self.general_layout.addLayout(self.title_layout)
        self.general_layout.addSpacing(20)
        self.general_layout.addLayout(self.form_layout)
        self.general_layout.addSpacing(20)
        self.general_layout.addLayout(self.button_layout)
        self.setLayout(self.general_layout)
        self.setMinimumWidth(600)
        # self.setWindowTitle('')

    def select_path(self):
        dir_choose = QFileDialog.getExistingDirectory(self, '选取文件夹', self.start_path, options=QFileDialog.DontUseNativeDialog)
        if dir_choose:
            self.rename_path_text.setText(dir_choose)

    def click_sure(self):
        self.setHidden(True)
        file_name = self.rename_text.text()
        if file_name == '':
            file_name = self.default_name
        rename_path = MergePath(self.rename_path_text.text(), file_name).merged_path
        if os.path.exists(rename_path):
            self.deal_existed_file(rename_path)
        else:
            self.deal_not_existed_file(rename_path)

    def click_cancel(self):
        self.setHidden(True)

    # 处理已经存在的文件(需要先添加警告)
    def deal_existed_file(self, rename_path):
        if os.path.isdir(self.source_path):
            reply = QMessageBox.question(self, '此文件夹已经存在', '是否合并这两个已经存在的文件？',
                                         QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.No)
            if reply == QMessageBox.No:
                self.setHidden(False)
            elif reply == QMessageBox.Yes:
                if rename_path != self.source_path:
                    for name in os.listdir(self.source_path):
                        if name not in os.listdir(rename_path):
                            current_path = MergePath(self.source_path, name).merged_path
                            if os.path.isdir(current_path):
                                shutil.copytree(current_path, MergePath(rename_path, name).merged_path)
                            else:
                                shutil.copyfile(current_path, MergePath(rename_path, name).merged_path)
                    os.removedirs(self.source_path)
                    # 发射重命名信号
                    self.signal.emit('rename_path>' + rename_path)
            else:
                pass
        else:
            reply = QMessageBox.question(self, '此文件已经存在', '是否替换已经存在的文件？',
                                         QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.No)
            if reply == QMessageBox.No:
                self.setHidden(False)
            elif reply == QMessageBox.Yes:
                if rename_path != self.source_path:
                    shutil.copyfile(self.source_path, rename_path)
                    os.remove(self.source_path)
                    # 发射重命名信号
                    self.signal.emit('rename_path>' + rename_path)
            else:
                pass

    def deal_not_existed_file(self, rename_path):
        os.rename(self.source_path, rename_path)
        # 发射重命名信号
        self.signal.emit('rename_path>' + rename_path)


# 删除文件
class Delete(QDialog):

    signal = pyqtSignal(str)

    def __init__(self, parent, path_list):
        super(Delete, self).__init__(parent)
        # 原路径
        self.path_list = path_list
        self.title = QLabel(self)
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setText('删除')
        self.h_line = QFrame(self)
        self.h_line.setFrameShape(QFrame.HLine)
        self.title_layout = QVBoxLayout()
        self.title_layout.addWidget(self.title)
        self.title_layout.addWidget(self.h_line)
        # 源文件路径(显示)
        self.source_path_text = QLabel(self)
        self.source_path_text.setStyleSheet(BeautifyStyle.label_qss)
        self.source_path_text.setText('\n'.join(self.path_list))
        # 删除文件的警告
        self.delete_warning_text = QLabel(self)
        self.delete_warning_text.setStyleSheet(BeautifyStyle.label_qss)
        self.delete_warning_text.setAlignment(Qt.AlignCenter)
        self.delete_warning_text.setText('确定要删除选中的'+str(len(self.path_list))+'个文件/文件夹吗？')
        # 确定和取消按钮
        self.sure_button = QPushButton('确定', self)
        self.sure_button.clicked.connect(self.click_sure)
        self.sure_button.setFixedWidth(100)
        self.cancel_button = QPushButton('取消', self)
        self.cancel_button.clicked.connect(self.click_cancel)
        self.cancel_button.setFixedWidth(100)
        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.sure_button)
        self.button_layout.addWidget(self.cancel_button)
        # 全局布局
        self.general_layout = QVBoxLayout(self)
        self.general_layout.setContentsMargins(0, 5, 0, 5)
        self.general_layout.addLayout(self.title_layout)
        self.general_layout.addSpacing(20)
        self.general_layout.addWidget(self.source_path_text)
        self.general_layout.addSpacing(20)
        self.general_layout.addWidget(self.delete_warning_text)
        self.general_layout.addSpacing(20)
        self.general_layout.addLayout(self.button_layout)
        self.setLayout(self.general_layout)
        self.setMinimumWidth(600)

    def click_sure(self):
        self.setHidden(True)
        for path in self.path_list:
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)
            self.signal.emit('delete_path>' + path)

    def click_cancel(self):
        self.setHidden(True)