import os
import operator
from threading import Thread
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from other.glv import Icon
from ui_class.TreeWidget import TreeWidget
import xml.etree.cElementTree as ET


class TreeStructure(QWidget):
    def __init__(self, parent, xml_file=None):
        super(TreeStructure, self).__init__(parent)
        # 传入的文件
        self.xml_file = xml_file
        # 保存上次的节点信息
        self.old_tree_data = []
        # tree_list保存所有树
        self.tree_list = []
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
        # QFrame(用来放置tree)
        frame_qss = 'border:1px solid #646464;'
        self.frame = QFrame(self)
        self.frame.setStyleSheet(frame_qss)
        self.frame_layout = QVBoxLayout(self.frame)
        self.frame_layout.setSpacing(0)
        self.frame_layout.setContentsMargins(0, 0, 0, 0)
        # 布局
        self.general_layout = QVBoxLayout()
        self.general_layout.setContentsMargins(0, 0, 0, 0)
        self.general_layout.setSpacing(0)
        self.general_layout.addWidget(self.title)
        self.general_layout.addWidget(self.frame)
        self.setLayout(self.general_layout)

    # 展开节点
    def expand_all_node(self):
        self.tree.expandAll()

    # 关闭节点
    def collapse_all_node(self):
        self.tree.collapseAll()

    # 加载结构树
    def load_tree(self, file):
        tree = TreeWidget(self, file)
        self.tree_list.append(tree)
        if self.frame_layout.count() != 0:
            self.tree.setHidden(True)
        self.frame_layout.addWidget(tree)
        self.tree = tree

    # 更新树
    def update_tree(self, file):
        file_list = [tree.file for tree in self.tree_list]
        if file in file_list:
            self.tree.setHidden(True)
            index = file_list.index(file)
            current_tree = self.tree_list[index]
            current_tree.setHidden(False)
            current_tree.update_structure(file)
            self.tree = current_tree
        else:
            self.load_tree(file)
