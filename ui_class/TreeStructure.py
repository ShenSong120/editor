import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from other.glv import Icon
import xml.etree.cElementTree as ET


class TreeStructure(QWidget):
    def __init__(self, parent, file='example'):
        super(TreeStructure, self).__init__(parent)
        # 设置背景色
        self.setStyleSheet('background-color: #F0F0F0; font-family:Arial;')
        # 控件title
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
        self.root = QTreeWidgetItem(self.tree)
        self.root.setText(0, file)

        self.update_structure(self.root)

        self.tree.addTopLevelItem(self.root)

        self.general_layout = QVBoxLayout()
        self.general_layout.setContentsMargins(0, 0, 0, 0)
        self.general_layout.setSpacing(0)
        self.general_layout.addWidget(self.title)
        self.general_layout.addWidget(self.tree)

        self.setLayout(self.general_layout)

    # 更新树形结构视图
    def update_structure(self, parent):
        file = 'D:/Code/editor/xml/test.xml'
        tree = ET.ElementTree(file=file)
        root = tree.getroot()
        parent = self.add_item(parent, root)
        for child_of_1 in root:
            child_of_1_as_root = self.add_item(parent, child_of_1)
            for child_of_2 in child_of_1:
                child_of_2_as_root = self.add_item(child_of_1_as_root, child_of_2)
                for child_of_3 in child_of_2:
                    child_of_3_as_root = self.add_item(child_of_2_as_root, child_of_3)
                    for child_of_4 in child_of_3:
                        child_of_4_as_root = self.add_item(child_of_3_as_root, child_of_4)
                        for child_of_5 in child_of_4:
                            child_of_5_as_root = self.add_item(child_of_4_as_root, child_of_5)
                            for child_of_6 in child_of_5:
                                self.add_item(child_of_5_as_root, child_of_6)

    # 添加节点
    def add_item(self, parent, info):
        tag = info.tag
        info_dict = info.attrib
        id_text = ''
        name_text = ''
        key_text = ''
        if len(info_dict):
            for key in info_dict.keys():
                if key == 'id':
                    id_text = info_dict[key]
                elif key == 'name':
                    name_text = info_dict[key]
                elif key == 'key':
                    key_text = 'key:' + info_dict[key]
        if 'id' in info_dict.keys():
            text = id_text + ':' + tag + ' name:' + name_text + ' ' + key_text
        else:
            if name_text == '':
                text = tag + ' ' + key_text
            else:
                text = name_text + ':' + tag + ' ' + key_text
        child = QTreeWidgetItem(parent)
        child.setText(0, text)
        child.setIcon(0, QIcon(Icon.xml_tag))
        return child
