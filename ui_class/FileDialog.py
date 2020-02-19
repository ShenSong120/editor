from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from glv import Icon


class NewFile(QDialog):
    def __init__(self, parent, path):
        super(NewFile, self).__init__(parent)
        # 新建文件起始路径
        self.path = path
        self.title = QLabel(self)
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setText('新建文件')
        self.h_line = QFrame(self)
        self.h_line.setFrameShape(QFrame.HLine)
        self.title_layout = QVBoxLayout()
        self.title_layout.addWidget(self.title)
        self.title_layout.addWidget(self.h_line)
        # 文件路径选择以及文件名字输入
        self.path_text = QLineEdit(self)
        self.path_text.setReadOnly(True)
        self.path_text.setText(self.path)
        self.select_path_action = QAction(self.path_text)
        self.select_path_action.setIcon(QIcon(Icon.path))
        self.select_path_action.triggered.connect(self.select_path)
        self.path_text.addAction(self.select_path_action, QLineEdit.TrailingPosition)
        self.file_name_text = QLineEdit(self)
        self.form_layout = QFormLayout()
        self.form_layout.setSpacing(20)
        self.form_layout.addRow('文件路径:', self.path_text)
        self.form_layout.addRow('文件名字:', self.file_name_text)
        # 确定和取消按钮
        self.sure_button = QPushButton('确定', self)
        self.sure_button.setFixedWidth(100)
        self.cancel_button = QPushButton('取消', self)
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
        dir_choose = QFileDialog.getExistingDirectory(self, '选取文件夹', self.path, options=QFileDialog.DontUseNativeDialog)
        if dir_choose:
            print(dir_choose)


class NewFolder(QDialog):
    def __init__(self, parent, path):
        super(NewFolder, self).__init__(parent)
        # 新建文件夹起始路径
        self.path = path
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
        self.path_text.setText(self.path)
        self.select_path_action = QAction(self.path_text)
        self.select_path_action.setIcon(QIcon(Icon.path))
        self.select_path_action.triggered.connect(self.select_path)
        self.path_text.addAction(self.select_path_action, QLineEdit.TrailingPosition)
        self.file_name_text = QLineEdit(self)
        self.form_layout = QFormLayout()
        self.form_layout.setSpacing(20)
        self.form_layout.addRow('文件夹路径:', self.path_text)
        self.form_layout.addRow('文件夹名字:', self.file_name_text)
        # 确定和取消按钮
        self.sure_button = QPushButton('确定', self)
        self.sure_button.setFixedWidth(100)
        self.cancel_button = QPushButton('取消', self)
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
        dir_choose = QFileDialog.getExistingDirectory(self, '选取文件夹', self.path, options=QFileDialog.DontUseNativeDialog)
        if dir_choose:
            print(dir_choose)


class NewXmlFile(QDialog):
    def __init__(self, parent, path):
        super(NewXmlFile, self).__init__(parent)
        # 新建xml文件起始路径
        self.path = path
        self.title = QLabel(self)
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setText('新建xml文件')
        self.h_line = QFrame(self)
        self.h_line.setFrameShape(QFrame.HLine)
        self.title_layout = QVBoxLayout()
        self.title_layout.addWidget(self.title)
        self.title_layout.addWidget(self.h_line)
        # xml文件路径选择以及xml文件名字输入
        self.path_text = QLineEdit(self)
        self.path_text.setReadOnly(True)
        self.path_text.setText(self.path)
        self.select_path_action = QAction(self.path_text)
        self.select_path_action.setIcon(QIcon(Icon.path))
        self.select_path_action.triggered.connect(self.select_path)
        self.path_text.addAction(self.select_path_action, QLineEdit.TrailingPosition)
        self.file_name_text = QLineEdit(self)
        self.form_layout = QFormLayout()
        self.form_layout.setSpacing(20)
        self.form_layout.addRow('xml文件路径:', self.path_text)
        self.form_layout.addRow('xml文件名字:', self.file_name_text)
        # 确定和取消按钮
        self.sure_button = QPushButton('确定', self)
        self.sure_button.setFixedWidth(100)
        self.cancel_button = QPushButton('取消', self)
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
        dir_choose = QFileDialog.getExistingDirectory(self, '选取文件夹', self.path, options=QFileDialog.DontUseNativeDialog)
        if dir_choose:
            print(dir_choose)