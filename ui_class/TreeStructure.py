import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class TreeStructure(QWidget):
    def __init__(self, parent):
        super(TreeStructure, self).__init__(parent)
        self.title = QLineEdit('Structure', self)
        self.title.setStyleSheet('height:24px; background:#99CCFF; border:2px solid #99CCFF;')
        self.tree = QTreeWidget(self)
        self.tree.setStyleSheet('border:1px solid transparent;')

        self.general_layout = QVBoxLayout()
        self.general_layout.setContentsMargins(0, 0, 0, 0)
        self.general_layout.setSpacing(0)
        self.general_layout.addWidget(self.title)
        self.general_layout.addWidget(self.tree)

        self.setLayout(self.general_layout)