from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from ui_class.FileDialog import NewFile, NewFolder, NewXmlFile


class New(QDialog):

    signal = pyqtSignal(str)

    def __init__(self, parent, path):
        super(New, self).__init__(parent)
        # 路径(新建文件以及文件夹时候的起始路径)
        self.path = path
        # title
        self.title = QLabel(self)
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setText('新建')
        # listWidget
        self.list_widget = QListWidget(self)
        self.new_items = ['文件', '文件夹', 'Xml文件']
        self.list_widget.addItems(self.new_items)
        self.list_widget.itemClicked.connect(self.item_clicked_action)
        self.general_layout = QVBoxLayout(self)
        self.general_layout.setContentsMargins(0, 5, 0, 0)
        self.general_layout.addWidget(self.title)
        self.general_layout.addWidget(self.list_widget)
        self.setLayout(self.general_layout)
        self.setWindowTitle('NEW')

    def item_clicked_action(self, item):
        self.setHidden(True)
        if item.text() == '文件':
            self.new_file()
        elif item.text() == '文件夹':
            self.new_folder()
        elif item.text() == 'Xml文件':
            self.new_xml_file()

    def new_file(self):
        self.new_file_dialog = NewFile(self, self.path)
        self.new_file_dialog.exec()
        self.signal.emit('new_file>')

    def new_folder(self):
        self.new_folder_dialog = NewFolder(self, self.path)
        self.new_folder_dialog.exec()
        self.signal.emit('new_folder>')

    def new_xml_file(self):
        self.new_xml_file_dialog = NewXmlFile(self, self.path)
        self.new_xml_file_dialog.exec()
        self.signal.emit('new_xml_file>')