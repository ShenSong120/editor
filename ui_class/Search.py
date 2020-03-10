from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
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
        self.search_line_edit.textChanged.connect(self.find_first_option)
        self.search_line_edit.setStyleSheet('background-color:#000000; color:white;')
        self.search_line_edit.setMinimumWidth(200)
        self.search_line_edit.setMaximumWidth(400)
        # 搜索框控件(敲击回车匹配下一个)
        self.find_first_action = QAction(self.search_line_edit)
        self.find_first_action.setShortcut('return')
        self.find_first_action.setIcon(QIcon(Icon.enter))
        self.find_first_action.triggered.connect(self.find_next_option)
        self.search_line_edit.addAction(self.find_first_action, QLineEdit.TrailingPosition)
        # 上一个
        self.last_option_button = QToolButton(self)
        self.last_option_button.clicked.connect(self.find_last_option)
        self.last_option_button.setToolTip('上一个搜索项')
        self.last_option_button.setStyleSheet('QToolButton{border-image: url(' + Icon.last + ')}')
        # 下一个
        self.next_option_button = QToolButton(self)
        self.next_option_button.clicked.connect(self.find_next_option)
        self.next_option_button.setToolTip('下一个搜索项')
        self.next_option_button.setStyleSheet('QToolButton{border-image: url(' + Icon.next + ')}')
        # 匹配数量
        self.match_num_label = QLabel(self)
        # self.match_num_label.setText('123')
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
        self.general_layout.addStretch(1)
        self.general_layout.addWidget(self.match_num_label)
        self.general_layout.addStretch(2)
        self.general_layout.addWidget(self.close_option_button)
        self.general_layout.addSpacing(30)
        self.setLayout(self.general_layout)

    # QLineEdit控件中的查找当前匹配
    def find_first_option(self):
        text = self.search_line_edit.text()
        self.parentWidget().findFirst(text, False, False, False, False, True, 0, 0, True)

    # 查找上一个匹配(暂时不支持)
    def find_last_option(self):
        text = self.search_line_edit.text()
        self.parentWidget().findFirst(text, False, False, False, True, False, -1, -1, True)
        self.parentWidget().findNext()

    # 查找下一个匹配
    def find_next_option(self):
        text = self.search_line_edit.text()
        # self.parentWidget().findNext()
        self.parentWidget().findFirst(text, False, False, False, True, True, -1, -1, True)

    # 关闭操作
    def close_option(self):
        self.setHidden(True)
        line, index = self.parentWidget().getCursorPosition()
        self.parentWidget().setCursorPosition(line, index)
