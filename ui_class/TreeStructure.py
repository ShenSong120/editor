import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from other.glv import Icon


class TreeStructure(QWidget):
    def __init__(self, parent, file='example'):
        super(TreeStructure, self).__init__(parent)
        self.title = QLineEdit('Structure', self)
        self.title.setStyleSheet('height:24px; background:#99CCFF; border:2px solid #99CCFF;')
        self.tree = QTreeWidget(self)
        tree_qss = 'border:1px solid transparent; \
                    QTreeWidget::branch:closed:has-children:!has-siblings, \
                    QTreeWidget::branch:closed:has-children:has-siblings \
                    {border-image:none; image:url(:/config/icon/root_close.png);} \
                    QTreeWidget::branch:open:has-children:!has-siblings, \
                    QTreeWidget::branch:open:has-children:has-siblings \
                    {border-image: none; image: url(:/config/icon/root_open.png);}'
        self.tree.setStyleSheet(tree_qss)
        self.tree.setHeaderHidden(True)

        # 设置列数
        self.tree.setColumnCount(1)
        # 设置根节点
        root = QTreeWidgetItem(self.tree)
        root.setText(0, file)

        child1 = QTreeWidgetItem(root)
        child1.setText(0, 'child1')

        self.tree.addTopLevelItem(root)

        self.general_layout = QVBoxLayout()
        self.general_layout.setContentsMargins(0, 0, 0, 0)
        self.general_layout.setSpacing(0)
        self.general_layout.addWidget(self.title)
        self.general_layout.addWidget(self.tree)

        self.setLayout(self.general_layout)