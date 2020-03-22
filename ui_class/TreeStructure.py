from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from other.glv import Icon
from ui_class.TreeWidget import TreeWidget


class TreeStructure(QWidget):
    def __init__(self, parent, file=None):
        super(TreeStructure, self).__init__(parent)
        # 传入的文件
        self.file = file
        # 设置背景色
        # self.setStyleSheet('background-color: #F0F0F0; font-family:Arial;')
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
        # 堆叠窗口
        stacked_widget_qss = 'border:1px solid #646464;'
        self.stacked_widget = QStackedWidget(self)
        self.stacked_widget.setStyleSheet(stacked_widget_qss)
        # 布局
        self.general_layout = QVBoxLayout()
        self.general_layout.setContentsMargins(0, 0, 0, 0)
        self.general_layout.setSpacing(0)
        self.general_layout.addWidget(self.title)
        self.general_layout.addWidget(self.stacked_widget)
        self.setLayout(self.general_layout)

    # 展开节点
    def expand_all_node(self):
        self.tree.expandAll()

    # 关闭节点
    def collapse_all_node(self):
        self.tree.collapseAll()

    # 加载结构树
    def load_tree(self, file):
        self.tree = TreeWidget(file)
        self.stacked_widget.addWidget(self.tree)
        self.stacked_widget.setCurrentWidget(self.tree)

    # 更新树
    def update_tree(self, file):
        file_list = [self.stacked_widget.widget(index).file for index in range(self.stacked_widget.count())]
        if file in file_list:
            index = file_list.index(file)
            self.tree = self.stacked_widget.widget(index)
            self.stacked_widget.setCurrentWidget(self.tree)
            self.tree.update_structure(file)
        else:
            self.load_tree(file)

    def close_tree(self):
        tree_list = [self.stacked_widget.widget(index) for index in range(self.stacked_widget.count())]
        for tree in tree_list:
            self.stacked_widget.removeWidget(tree)
        self.tree.clear()
