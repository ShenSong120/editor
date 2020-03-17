import os
import sys
from collections import OrderedDict
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
        # 保存上一次的树数据
        self.old_tree_data = []
        # 子节点
        self.child_list = []
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

    # 添加节点
    def add_node(self, parent=None, node_name=None):
        child = QTreeWidgetItem(parent)
        child.setText(0, node_name)
        child.setIcon(0, QIcon(Icon.xml_tag))
        return child

    # 获取节点name
    def get_node_name(self, tag, attrib):
        text = tag
        # 如果存在属性
        if len(attrib):
            for key in attrib.keys():
                if key == 'id':
                    text = attrib[key] + ':' + text
                elif key == 'name':
                    if 'id' in attrib.keys():
                        text = text + ' name:' + attrib[key]
                    else:
                        text = attrib[key] + ':' + text
                else:
                    text = text + ' ' + key + ':' + attrib[key]
        return text

    # 节点遍历
    def node_traverse(self, root_node, level, result_list):
        temp_list = [level, root_node.tag, root_node.attrib]
        result_list.append(temp_list)
        # 遍历每个子节点
        children_node = root_node.getchildren()
        if len(children_node) == 0:
            return
        for child in children_node:
            self.node_traverse(child, level + 1, result_list)
        return

    # 获取树数据
    def get_tree_data(self, xml_file):
        # 保存树数据
        result_list = []
        try:
            # 根据xml文本获取子节点
            tree = ET.ElementTree(file=xml_file)
            xml_root = tree.getroot()
            level = 0  # 节点的深度从0开始(0是case标签)
            self.node_traverse(xml_root, level, result_list)
        except ET.ParseError:
            pass
        except FileNotFoundError:
            pass
        finally:
            return result_list

    # 新建树结构
    def new_structure(self, tree_data):
        for note_data in tree_data:
            level, tag, attrib = note_data
            node_name = self.get_node_name(tag, attrib)
            if level == 0:
                xml_root = self.add_node(self.root, node_name)
                self.child_list.append(xml_root)
            elif level == 1:
                first_node = self.add_node(xml_root, node_name)
                self.child_list.append(first_node)
            elif level == 2:
                second_node = self.add_node(first_node, node_name)
                self.child_list.append(second_node)
            elif level == 3:
                third_node = self.add_node(second_node, node_name)
                self.child_list.append(third_node)
            elif level == 4:
                fourth_node = self.add_node(third_node, node_name)
                self.child_list.append(fourth_node)
            elif level == 5:
                fifth_node = self.add_node(fourth_node, node_name)
                self.child_list.append(fifth_node)
            elif level == 6:
                sixth_node = self.add_node(fifth_node, node_name)
                self.child_list.append(sixth_node)

    # 动态更新结构图
    def dynamic_update_structure(self, current_tree_data):
        old_tree_data_length = len(self.old_tree_data)
        current_tree_data_length = len(current_tree_data)
        # 增加标签
        if current_tree_data_length > old_tree_data_length:
            for i in range(current_tree_data_length):
                if current_tree_data[i] not in self.old_tree_data:
                    level, tag, attrib = current_tree_data[i]
                    node_name = self.get_node_name(tag, attrib)
                    child = self.add_node(node_name=node_name)
                    if level == 1:
                        previous_level = current_tree_data[i-1][0]
                        if previous_level == 1:
                            index = self.root.child(0).indexOfChild(self.child_list[i-1])
                        self.root.child(0).insertChild(index+1, child)
                        self.child_list.insert(i, child)
        # 删除标签
        elif current_tree_data_length < old_tree_data_length:
            pass
        # 更改标签
        elif current_tree_data_length == old_tree_data_length:
            pass

    # 更新树形结构视图
    def update_structure(self, xml_file):
        self.xml_file = xml_file
        title = 'None' if xml_file == 'None' else os.path.split(xml_file)[1]
        self.root.setText(0, title)
        current_tree_data = self.get_tree_data(xml_file)
        current_tree_data = self.old_tree_data if len(current_tree_data) == 0 else current_tree_data
        if len(self.old_tree_data) == 0:
            self.new_structure(current_tree_data)
            self.old_tree_data = current_tree_data
            return
        # 动态更新
        self.dynamic_update_structure(current_tree_data)
        # 保存数据
        self.old_tree_data = current_tree_data
