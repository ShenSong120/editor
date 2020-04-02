import os
import operator
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from glv import Icon
import xml.etree.cElementTree as ET


# 自定义的item 继承自QListWidgetItem
class CustomQTreeWidgetItem(QTreeWidgetItem):
    def __init__(self, icon, text, parent=None):
        super(CustomQTreeWidgetItem, self).__init__(parent)
        # 自定义item中的widget 用来显示自定义的内容 font-size: 11pt;
        self.widget = QWidget()
        # 传递进来的文本(非富文本)
        self.string_text = text
        # 用来显示name
        self.text_label = QLabel()
        self.setText(0, self.string_text)
        # 用来显示icon(图像)
        self.icon_label = QLabel()
        # 设置图像源 和 图像大小
        self.icon_label.setPixmap(QPixmap(icon).scaled(24, 24))
        # 设置布局用来对text_label和icon_abel进行布局
        self.h_box = QHBoxLayout()
        self.h_box.setSpacing(0)
        self.h_box.setContentsMargins(0, 0, 0, 0)
        self.h_box.addWidget(self.icon_label)
        self.h_box.addSpacing(3)
        self.h_box.addWidget(self.text_label)
        self.h_box.addStretch(1)
        # 设置widget的布局
        self.widget.setLayout(self.h_box)

    def setText(self, p_int, p_str):
        self.string_text = p_str
        if ' ' in p_str:
            first_half_text = p_str.split(' ')[0]
            second_half_text = ' '.join(p_str.split(' ')[1:])
        else:
            first_half_text = p_str
            second_half_text = ''
        rich_text = '<font color = "#242424">' + first_half_text + ' ' + '</font>' + \
                    '<font color = "#808080"><i>' + second_half_text + '</i></font>'
        self.text_label.setText(rich_text)

    def text(self, p_int):
        return self.string_text


# QTreeWidget
class TreeWidget(QWidget):
    signal = pyqtSignal(str)

    def __init__(self, file):
        super(TreeWidget, self).__init__()
        self.file = file
        # QWidget背景透明
        self.setStyleSheet('background-color: transparent;')
        # transparent
        tree_qss = 'border:0px solid #646464; \
                    QTreeWidget::branch:closed:has-children:!has-siblings, \
                    QTreeWidget::branch:closed:has-children:has-siblings \
                    {border-image:none; image:url(:/config/icon/root_close.png);} \
                    QTreeWidget::branch:open:has-children:!has-siblings, \
                    QTreeWidget::branch:open:has-children:has-siblings \
                    {border-image: none; image: url(:/config/icon/root_open.png);}'
        self.tree = QTreeWidget()
        self.tree.setStyleSheet(tree_qss)
        self.tree.setHeaderHidden(True)
        # 设置列数
        self.tree.setColumnCount(1)
        # 设置根节点(默认无任何节点)
        self.root_name = os.path.split(self.file)[1]
        self.root = QTreeWidgetItem()
        self.root.setIcon(0, QIcon(Icon.file))
        self.root.setText(0, self.root_name)
        self.tree.addTopLevelItem(self.root)
        self.root.setExpanded(True)
        # 当前修改后的xml信息
        self.old_tree_data = []
        # 加载树结构
        self.current_tree_data = self.get_tree_data(self.file)
        # item选中项改变触发事件
        self.tree.itemSelectionChanged.connect(self.item_selection_changed)
        # widget布局
        self.h_layout = QHBoxLayout()
        self.h_layout.setSpacing(0)
        self.h_layout.setContentsMargins(0, 0, 0, 0)
        self.h_layout.addWidget(self.tree)
        self.setLayout(self.h_layout)

    # 添加节点
    def add_node(self, parent=None, node_name=None):
        child = CustomQTreeWidgetItem(Icon.xml_tag, node_name, parent)
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
            self.tree.setItemWidget(child, 0, child.widget)

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
        self.file = xml_file
        self.root_name = os.path.split(xml_file)[1]
        self.root.setText(0, self.root_name)
        # 获取当前信息
        current_tree_data = self.get_tree_data(xml_file)
        # 正在修改xml(会报错返回一个元素-1)
        if len(current_tree_data) == 1 and current_tree_data[0] == -1:
            pass
        # 更新树结构
        else:
            self.update_node(current_tree_data)

    # item选中项改变触发事件
    def item_selection_changed(self):
        item = self.tree.currentItem()
        if item is self.root:
            return
        position = []
        for i in range(10):
            parent_item = item.parent()
            if parent_item:
                index = parent_item.indexOfChild(item)
                position.insert(0, index)
                item = parent_item
            else:
                break
        # 找到当前item的信息
        for item_info in self.old_tree_data:
            if item_info[0] == position:
                target_item = item_info
                break
        # 获取相同item
        same_item = []
        for item_info in self.old_tree_data:
            if target_item[1:] == item_info[1:]:
                same_item.append(item_info)
        # 需要find的次数
        target_index = same_item.index(target_item) + 1
        # 根据正则匹配
        target_item = target_item
        # print(target_index, target_item)
        # 正则表达式
        # <action\s+name\s?=\s?"inputText"\s+key\s?=\s?"click"\s?>
        regex = '<\\s?' + target_item[1]
        for key, value in target_item[2].items():
            regex = regex + '\\s+' + key + '\\s?=\\s?"' + value + '"'
        regex = regex + '\\s?>'
        self.signal.emit('find_current_item/' + str([target_index, regex]))
        # print(target_index, regex)
