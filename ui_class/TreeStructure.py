from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from glv import Icon
from ui_class.TreeWidget import TreeWidget


class TreeStructure(QWidget):
    signal = pyqtSignal(str)

    def __init__(self, parent, file=None):
        super(TreeStructure, self).__init__(parent)
        # 传入的文件
        self.file = file
        # 设置背景色
        self.setStyleSheet('font-family:Arial;')
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
        self.tree_eidget.tree.expandAll()

    # 关闭节点
    def collapse_all_node(self):
        self.tree_eidget.tree.collapseAll()

    # 加载结构树
    def load_tree(self, file):
        self.tree_eidget = TreeWidget(file)
        self.tree_eidget.signal[str].connect(self.get_signal_from_tree)
        self.stacked_widget.addWidget(self.tree_eidget)
        self.stacked_widget.setCurrentWidget(self.tree_eidget)
        # (如果文件有错误, 返回一个-1元素, 将产生的信息生成structure-tree)
        if self.tree_eidget.current_tree_data[0] != -1:
            self.tree_eidget.insert_child(self.tree_eidget.current_tree_data)
            self.tree_eidget.old_tree_data = self.tree_eidget.current_tree_data

    # 更新树
    def update_tree(self, file):
        file_list = [self.stacked_widget.widget(index).file for index in range(self.stacked_widget.count())]
        if file in file_list:
            index = file_list.index(file)
            self.tree_eidget = self.stacked_widget.widget(index)
            self.stacked_widget.setCurrentWidget(self.tree_eidget)
            self.tree_eidget.update_structure(file)
        else:
            self.load_tree(file)

    def close_tree(self):
        tree_list = [self.stacked_widget.widget(index) for index in range(self.stacked_widget.count())]
        for tree in tree_list:
            self.stacked_widget.removeWidget(tree)

    # 从tree结构获取信号
    def get_signal_from_tree(self, signal_str):
        self.signal.emit(signal_str)
