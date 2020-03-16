import os
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from other.glv import Icon
import xml.etree.cElementTree as ET


class TreeStructure(QWidget):
    def __init__(self, parent, xml_file=None):
        super(TreeStructure, self).__init__(parent)
        # 传入的文件
        self.xml_file = xml_file
        # 设置背景色
        self.setStyleSheet('background-color: #F0F0F0; font-family:Arial;')
        # 控件title
        self.title = QLineEdit('Structure', self)
        self.title.setStyleSheet('height:25px; background:#99CCFF; border:1px solid #646464;')
        self.tree = QTreeWidget(self)
        # transparent
        tree_qss = 'border:1px solid #646464; \
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
        # 设置根节点(默认无任何节点)
        self.root = QTreeWidgetItem(self.tree)
        self.root.setText(0, 'None')
        # 设置根节点
        self.tree.addTopLevelItem(self.root)
        # 布局
        self.general_layout = QVBoxLayout()
        self.general_layout.setContentsMargins(0, 0, 0, 0)
        self.general_layout.setSpacing(0)
        self.general_layout.addWidget(self.title)
        self.general_layout.addWidget(self.tree)

        self.setLayout(self.general_layout)

    # 更新树形结构视图
    def update_structure(self, xml_file):
        self.tree.clear()
        self.xml_file = xml_file
        # 重命名根节点名字(当前文件名)
        root_name = 'None' if self.xml_file == 'None' else os.path.split(self.xml_file)[1]
        self.root = QTreeWidgetItem(self.tree)
        self.root.setText(0, root_name)
        self.tree.addTopLevelItem(self.root)
        try:
            # 根据xml文本获取子节点
            tree = ET.ElementTree(file=self.xml_file)
            root = tree.getroot()
            # 添加xml根标签(文件名节点之下)
            parent = self.add_item(self.root, root)
            # 通过遍历添加子节点
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
        except ET.ParseError:
            pass
        except FileNotFoundError:
            pass

    # 添加节点
    def add_item(self, parent, info):
        tag = info.tag
        info_dict = info.attrib
        text = tag
        # 如果存在属性
        if len(info_dict):
            for key in info_dict.keys():
                if key == 'id':
                    text = info_dict[key] + ':' + text
                elif key == 'name':
                    if 'id' in info_dict.keys():
                        text = text + ' name:' + info_dict[key]
                    else:
                        text = info_dict[key] + ':' + text
                else:
                    text = text + ' ' + key + ':' + info_dict[key]
        child = QTreeWidgetItem(parent)
        child.setText(0, text)
        child.setIcon(0, QIcon(Icon.xml_tag))
        return child
