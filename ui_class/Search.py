from PyQt5.QtWidgets import *
from other.glv import Icon


class SearchBox(QFrame):
    def __init__(self, parent):
        super(SearchBox, self).__init__(parent)
        # 设置透明度
        self.effect = QGraphicsOpacityEffect()
        self.setGraphicsEffect(self.effect)
        self.effect.setOpacity(0.7)
        # self.setWindowTitle("子窗口")
        self.setStyleSheet('background-color:#CCCCCC;')
        # 搜索框
        self.search_line_edit = QLineEdit(self)
        self.search_line_edit.setStyleSheet('background-color:#333333;')
        self.search_line_edit.setMinimumWidth(200)
        self.search_line_edit.setMaximumWidth(400)
        # 上一个
        self.last_option_button = QToolButton(self)
        self.last_option_button.setToolTip('上一个搜索项')
        self.last_option_button.setStyleSheet('QToolButton{border-image: url(' + Icon.last + ')}')
        # 下一个
        self.next_option_button = QToolButton(self)
        self.next_option_button.setToolTip('下一个搜索项')
        self.next_option_button.setStyleSheet('QToolButton{border-image: url(' + Icon.next + ')}')
        # 关闭按钮
        self.close_option_button = QToolButton(self)
        self.close_option_button.setToolTip('关闭搜索框')
        self.close_option_button.setStyleSheet('QToolButton{border-image: url(' + Icon.close + ')}')
        self.close_option_button.clicked.connect(self.close_option)
        # 布局
        self.general_layout = QHBoxLayout(self)
        self.general_layout.setContentsMargins(0, 0, 5, 0)
        self.general_layout.addSpacing(80)
        self.general_layout.addWidget(self.search_line_edit)
        self.general_layout.addStretch(1)
        self.general_layout.addWidget(self.last_option_button)
        self.general_layout.addSpacing(20)
        self.general_layout.addWidget(self.next_option_button)
        self.general_layout.addStretch(2)
        self.general_layout.addWidget(self.close_option_button)
        self.general_layout.addSpacing(30)
        self.setLayout(self.general_layout)

    # 关闭操作
    def close_option(self):
        self.setHidden(True)
