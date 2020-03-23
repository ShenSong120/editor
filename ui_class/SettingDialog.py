from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class Setting(QDialog):
    def __init__(self, parent):
        super(Setting, self).__init__(parent=parent)
        self.setWindowTitle('设置')

        self.stacked_widget_1 = StackedWidget()
        self.stacked_widget_2 = StackedWidget()
        self.stacked_widget_3 = StackedWidget()

        self.tab_widget = QTabWidget(self)
        tab_widget_qss = 'QTabWidget:pane{border: 1px solid #7A7A7A; top: -1px;}\
                          QTabWidget:tab-bar{border: 1px solid blue; top: 0px; alignment:left; background: blue}\
                          QTabBar::tab{height: 25px; margin-right: 0px; margin-bottom:-3px; padding-left: 5px; padding-right: 5px;}\
                          QTabBar::tab:selected{border: 1px solid #0099FF; color: #0099FF; background-color: white; border-top: 1px solid #0099FF; border-bottom: 5px solid #0099FF;}\
                          QTabBar::tab:!selected{border: 1px solid #7A7A7A;}\
                          QTabBar::tab:!selected:hover{border: 1px solid #7A7A7A; color: #0099CC;}'
        self.tab_widget.setStyleSheet(tab_widget_qss)
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
        self.text_edit = QTextEdit(self)
        self.text_edit.setStyleSheet('font-family:Consolas;')
        metrics = QFontMetrics(self.text_edit.font())
        self.text_edit.setTabStopWidth(4 * metrics.width(' '))
        self.text_edit.ensureCursorVisible()
        self.text_edit.setLineWrapMode(QTextEdit.FixedPixelWidth)
        self.text_edit.setWordWrapMode(QTextOption.NoWrap)
        self.text_edit.setText('1234')
        self.stacked_widget = QStackedWidget(self)
        self.stacked_widget.addWidget(self.text_edit)
        # 底部按钮
        self.add_button = QPushButton('添加')
        self.modify_button = QPushButton('修改')
        self.delete_button = QPushButton('删除')
        self.save_button = QPushButton('保存')
        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.add_button)
        self.button_layout.addStretch(1)
        self.button_layout.addWidget(self.modify_button)
        self.button_layout.addStretch(1)
        self.button_layout.addWidget(self.save_button)
        self.button_layout.addStretch(1)
        self.button_layout.addWidget(self.delete_button)
        # 布局
        self.h_layout = QHBoxLayout()
        self.h_layout.setSpacing(0)
        self.h_layout.setContentsMargins(0, 0, 0, 0)
        self.h_layout.addWidget(self.list_widget)
        self.h_layout.addWidget(self.stacked_widget)
        self.h_layout.setStretch(0, 1)
        self.h_layout.setStretch(1, 1)
        # 整体布局
        self.general_layout = QVBoxLayout()
        self.general_layout.setSpacing(0)
        self.general_layout.setContentsMargins(0, 0, 0, 0)
        self.general_layout.addLayout(self.h_layout)
        self.general_layout.addLayout(self.button_layout)
        self.setLayout(self.general_layout)
