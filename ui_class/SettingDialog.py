from PyQt5.QtWidgets import *


class Setting(QDialog):
    def __init__(self, parent):
        super(Setting, self).__init__(parent=parent)

        self.stacked_widget_1 = StackedWidget()
        self.stacked_widget_2 = StackedWidget()
        self.stacked_widget_3 = StackedWidget()

        self.tab_widget = QTabWidget(self)
        self.tab_widget.addTab(self.stacked_widget_1, '标签')
        self.tab_widget.addTab(self.stacked_widget_2, '属性')
        self.tab_widget.addTab(self.stacked_widget_3, '代码块')

        self.general_layout = QHBoxLayout()
        self.general_layout.setSpacing(0)
        self.general_layout.setContentsMargins(0, 0, 0, 0)
        self.general_layout.addWidget(self.tab_widget)

        self.setLayout(self.general_layout)


class StackedWidget(QWidget):
    def __init__(self, parent=None):
        super(StackedWidget, self).__init__(parent=parent)
        # 装入自定义文件
        self.list_widget = QListWidget(self)
        self.list_widget.addItem('Basic Info')
        self.list_widget.addItem('Contact Info')
        self.list_widget.addItem('More Info')
        # 堆叠窗口
        self.label = QLabel(self)
        self.label.setText('1234')
        self.stacked_widget = QStackedWidget(self)
        self.stacked_widget.addWidget(self.label)

        self.general_layout = QHBoxLayout()
        self.general_layout.setSpacing(0)
        self.general_layout.setContentsMargins(0, 0, 0, 0)
        self.general_layout.addWidget(self.list_widget)
        self.general_layout.addWidget(self.stacked_widget)
        self.general_layout.setStretch(0, 1)
        self.general_layout.setStretch(1, 1)
        self.setLayout(self.general_layout)
