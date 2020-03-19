import os
import operator
from threading import Thread
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from other.glv import Icon
import xml.etree.cElementTree as ET


class TreeStructure(QWidget):
    def __init__(self, parent, xml_file=None):
        super(TreeStructure, self).__init__(parent)
        # 传入的文件
        self.xml_file = xml_file
        # 保存上次的节点信息
        self.old_tree_data = []
        # 子节点
        self.child_list = []
        # 设置背景色
        self.setStyleSheet('background-color: #F0F0F0; font-family:Arial;')
        # 控件title
        self.title = QLineEdit('Structure', self)
        self.title.setReadOnly(True)
        self.title.setStyleSheet('height:25px; background:#99CCFF; border:1px solid #646464;')
        # 关闭节点action
        self.collapse_action = QAction(self.title)
        self.collapse_action.setToolTip('关闭所有节点')
        self.collapse_action.setIcon(QIcon(Icon.collapse))
        self.collapse_action.triggered.connect(self.collapse_all_node)
        self.title.addAction(self.collapse_action, QLineEdit.TrailingPosition)
        # 展开节点action
        self.expand_action = QAction(self.title)
        self.expand_action.setToolTip('展开所有节点')
        self.expand_action.setIcon(QIcon(Icon.expand))
        self.expand_action.triggered.connect(self.expand_all_node)
        self.title.addAction(self.expand_action, QLineEdit.TrailingPosition)
        # 树形结构
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

    # 展开节点
    def expand_all_node(self):
        self.tree.expandAll()

    # 关闭节点
    def collapse_all_node(self):
        self.tree.collapseAll()

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

    # 获取解析后的xml数据列表
    def get_xml_data(self, root_node):
        result_list = []
        root_position = [0]
        root_info_list = [root_position, root_node.tag, root_node.attrib]
        result_list.append(root_info_list)
        first_node_list = root_node.getchildren()
        for first_node in first_node_list:
            first_index = first_node_list.index(first_node)
            first_position = root_position[:]
            first_position.append(first_index)
            result_list.append([first_position, first_node.tag, first_node.attrib])
            second_node_list = first_node.getchildren()
            for second_node in second_node_list:
                second_index = second_node_list.index(second_node)
                second_position = first_position[:]
                second_position.append(second_index)
                result_list.append([second_position, second_node.tag, second_node.attrib])
                third_node_list = second_node.getchildren()
                for third_node in third_node_list:
                    third_index = third_node_list.index(third_node)
                    third_position = second_position[:]
                    third_position.append(third_index)
                    result_list.append([third_position, third_node.tag, third_node.attrib])
                    fourth_node_list = third_node.getchildren()
                    for fourth_node in fourth_node_list:
                        fourth_index = fourth_node_list.index(fourth_node)
                        fourth_position = third_position[:]
                        fourth_position.append(fourth_index)
                        result_list.append([fourth_position, fourth_node.tag, fourth_node.attrib])
                        fifth_node_list = fourth_node.getchildren()
                        for fifth_node in fifth_node_list:
                            fifth_index = fifth_node_list.index(fifth_node)
                            fifth_position = fourth_position[:]
                            fifth_position.append(fifth_index)
                            result_list.append([fifth_position, fifth_node.tag, fifth_node.attrib])
                            sixth_node_list = fifth_node.getchildren()
                            for sixth_node in sixth_node_list:
                                sixth_index = sixth_node_list.index(sixth_node)
                                sixth_position = fifth_position[:]
                                sixth_position.append(sixth_index)
                                result_list.append([sixth_position, sixth_node.tag, sixth_node.attrib])
                                seventh_node_list = sixth_node.getchildren()
                                for seventh_node in seventh_node_list:
                                    seventh_index = seventh_node_list.index(seventh_node)
                                    seventh_position = sixth_position[:]
                                    seventh_position.append(seventh_index)
                                    result_list.append([seventh_position, seventh_node.tag, seventh_node.attrib])
                                    eighth_node_list = seventh_node.getchildren()
                                    for eighth_node in eighth_node_list:
                                        eighth_index = eighth_node_list.index(eighth_node)
                                        eighth_position = seventh_position[:]
                                        eighth_position.append(eighth_index)
                                        result_list.append([eighth_position, eighth_node.tag, eighth_node.attrib])
        return result_list

    # 获取树数据
    def get_tree_data(self, xml_file):
        # 保存树数据
        result_list = []
        try:
            # 根据xml文本获取子节点
            tree = ET.ElementTree(file=xml_file)
            xml_root = tree.getroot()
            result_list = self.get_xml_data(xml_root)
        except ET.ParseError:
            result_list = [-1]
        except FileNotFoundError:
            result_list = [-1]
        finally:
            return result_list

    # 新建树结构
    def new_structure(self, tree_data):
        self.child_list = []
        for note_data in tree_data:
            level, tag, attrib = note_data
            level = len(level) - 1
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

    # 插入子控件
    def insert_child(self, node_list):
        for node in node_list:
            position = node[0]
            node_level = len(position)
            parent = self.root
            for i in range(node_level - 1):
                parent = parent.child(position[i])
            node_name = self.get_node_name(node[1], node[2])
            child = self.add_node(node_name=node_name)
            parent.insertChild(position[-1], child)

    # 删除子控件
    def remove_child(self, node_list):
        node_list = sorted(node_list, key=lambda i:len(i[0]), reverse=True)
        child_list = []
        for node in node_list:
            position = node[0]
            node_level = len(position)
            child = self.root
            for i in range(node_level):
                child = child.child(position[i])
            # 通过控件信息找到item控件(将所有控件集合起来)
            child_list.append(child)
        for child in child_list:
            child.parent().removeChild(child)

    # 更新节点
    def update_child(self, current_node):
        position = current_node[0]
        node_level = len(position)
        child = self.root
        for i in range(node_level):
            child = child.child(position[i])
        child_text = self.get_node_name(current_node[1], current_node[2])
        child.setText(0, child_text)

    # 更新树信息
    def update_node(self, current_tree_data):
        old_tree_data_length = len(self.old_tree_data)
        current_tree_data_length = len(current_tree_data)
        if old_tree_data_length == 0:
            self.new_structure(current_tree_data)
            self.old_tree_data = current_tree_data
        else:
            # 增加节点
            if current_tree_data_length > old_tree_data_length:
                node_num = current_tree_data_length - old_tree_data_length
                for index in range(current_tree_data_length):
                    if index < old_tree_data_length:
                        if operator.eq(current_tree_data[index], self.old_tree_data[index]) is False:
                            start_index = index
                            end_index = start_index + node_num
                            node_list = [current_tree_data[i] for i in range(start_index, end_index)]
                            self.insert_child(node_list)
                            break
                    else:
                        start_index = index
                        end_index = start_index + node_num
                        node_list = [current_tree_data[i] for i in range(start_index, end_index)]
                        self.insert_child(node_list)
                        break
            # 删除节点
            elif old_tree_data_length > current_tree_data_length:
                node_num = old_tree_data_length - current_tree_data_length
                for index in range(old_tree_data_length):
                    if index < current_tree_data_length:
                        if operator.eq(self.old_tree_data[index], current_tree_data[index]) is False:
                            start_index = index
                            end_index = index + node_num
                            node_list = [self.old_tree_data[i] for i in range(start_index, end_index)]
                            self.remove_child(node_list)
                            break
                    else:
                        start_index = index
                        end_index = index + node_num
                        node_list = [self.old_tree_data[i] for i in range(start_index, end_index)]
                        self.remove_child(node_list)
                        break
            # 修改节点
            elif old_tree_data_length == current_tree_data_length:
                for index in range(old_tree_data_length):
                    if operator.eq(self.old_tree_data[index], current_tree_data[index]) is False:
                        current_node = current_tree_data[index]
                        self.update_child(current_node)
                        break
        self.old_tree_data = current_tree_data

    # 更新树形结构视图
    def update_structure(self, xml_file):
        self.xml_file = xml_file
        # 更新文件名
        title = 'None' if xml_file == 'None' else os.path.split(xml_file)[1]
        self.root.setText(0, title)
        if title != self.root.text(0):
            self.old_tree_data = []
        # 获取当前信息
        current_tree_data = self.get_tree_data(xml_file)
        # 正在修改xml(会报错返回一个元素-1)
        if len(current_tree_data) == 1 and current_tree_data[0] == -1:
            pass
        # 更新树结构
        else:
            self.update_node(current_tree_data)
