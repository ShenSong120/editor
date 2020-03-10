from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from other.glv import Icon


class ReplaceBox(QFrame):
    def __init__(self, parent):
        super(ReplaceBox, self).__init__(parent)
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
        # 搜索框内清除文本控件(点击清除文本)
        self.clear_search_edit_action = QAction(self.search_line_edit)
        self.clear_search_edit_action.setIcon(QIcon(Icon.clear_text))
        self.clear_search_edit_action.triggered.connect(self.clear_search_edit_text)
        self.search_line_edit.addAction(self.clear_search_edit_action, QLineEdit.TrailingPosition)
        # 搜索框回车控件(敲击回车匹配下一个)
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
        # 替代文本框
        self.replace_line_edit = QLineEdit(self)
        self.replace_line_edit.setStyleSheet('background-color:#000000; color:white;')
        self.replace_line_edit.setMinimumWidth(200)
        self.replace_line_edit.setMaximumWidth(400)
        # 替换框内清除文本控件(点击清除文本)
        self.clear_replace_edit_action = QAction(self.replace_line_edit)
        self.clear_replace_edit_action.setIcon(QIcon(Icon.clear_text))
        self.clear_replace_edit_action.triggered.connect(self.clear_replace_edit_text)
        self.replace_line_edit.addAction(self.clear_replace_edit_action, QLineEdit.TrailingPosition)
        # 替代框回车控件(敲击回车匹配下一个)
        self.replace_first_action = QAction(self.replace_line_edit)
        self.replace_first_action.setShortcut('return')
        self.replace_first_action.setIcon(QIcon(Icon.enter))
        # self.replace_first_action.triggered.connect(self.find_next_option)
        self.replace_line_edit.addAction(self.find_first_action, QLineEdit.TrailingPosition)
        # 替换按钮
        self.replace_button = QPushButton('替换', self)
        self.replace_all_button = QPushButton('替换所有', self)
        button_style = 'QPushButton{border-radius:8px; border:3px solid #000000; padding:2px 6px 0px 6px;}'
        self.replace_button.setStyleSheet(button_style)
        self.replace_all_button.setStyleSheet(button_style)
        # 搜索结果背景标记
        self.search_thread = SearchThread()
        self.search_thread.signal[str].connect(self.search_option_marker)
        # search布局
        self.search_layout = QHBoxLayout()
        self.search_layout.setContentsMargins(0, 0, 5, 0)
        self.search_layout.addSpacing(80)
        self.search_layout.addWidget(self.search_line_edit)
        self.search_layout.addStretch(1)
        self.search_layout.addWidget(self.last_option_button)
        self.search_layout.addSpacing(20)
        self.search_layout.addWidget(self.next_option_button)
        self.search_layout.addStretch(1)
        self.search_layout.addWidget(self.match_num_label)
        self.search_layout.addStretch(6)
        self.search_layout.addWidget(self.close_option_button)
        self.search_layout.addSpacing(30)
        # replace布局
        self.replace_layout = QHBoxLayout()
        self.replace_layout.setContentsMargins(0, 0, 5, 0)
        self.replace_layout.addSpacing(80)
        self.replace_layout.addWidget(self.replace_line_edit)
        self.replace_layout.addStretch(1)
        self.replace_layout.addWidget(self.replace_button)
        self.replace_layout.addSpacing(20)
        self.replace_layout.addWidget(self.replace_all_button)
        self.replace_layout.addStretch(9)
        # 总体布局
        self.general_layout = QVBoxLayout(self)
        self.general_layout.setContentsMargins(0, 0, 0, 0)
        self.general_layout.addLayout(self.search_layout)
        self.general_layout.addLayout(self.replace_layout)

        self.setLayout(self.general_layout)

    def clear_search_edit_text(self):
        self.search_line_edit.clear()

    def clear_replace_edit_text(self):
        self.replace_line_edit.clear()

    # 明确指标
    def clear_indicators(self, indicator):
        self.parentWidget().clearIndicatorRange(0, 0, self.parentWidget().lines(), 0, indicator)

    # 搜索结果北京标记
    def search_option_marker(self, signal_str):
        palabras = eval(signal_str)
        self.clear_indicators(self.parentWidget().WORD_INDICATOR)
        for p in palabras:
            self.parentWidget().fillIndicatorRange(p[0], p[1], p[0], p[2], self.parentWidget().WORD_INDICATOR)
        if len(palabras) == 1:
            if sum(palabras[0]) == 0:
                self.match_num_label.setText('No matches')
                return
        char = str(len(palabras))
        self.match_num_label.setText(char+' matches')

    # QLineEdit控件中的查找当前匹配
    def find_first_option(self):
        text = self.search_line_edit.text()
        self.search_thread.find(text, self.parentWidget().text())
        flag = self.parentWidget().findFirst(text, False, False, False, False, True, 0, 0, True)
        if flag is False:
            line, index = self.parentWidget().getCursorPosition()
            self.parentWidget().setCursorPosition(line, index)

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


# 渲染线程(将目标文字背景变色)
class SearchThread(QThread):
    signal = pyqtSignal(str)

    def run(self):
        found_list = []
        # 需要判断搜索文本是否为空
        if self._word != '':
            found_generator = self.find_with_lines(self._text, self._word)
            for i in found_generator:
                found_list.append([i[2], i[0], i[1]])
        else:
            found_list.append([0, 0, 0])
        self.signal.emit(str(found_list))

    def find_with_lines(self, text, word):
        for line_number, line in enumerate(text.splitlines()):
            for index, end in self.ffind(line, word):
                yield index, end, line_number

    def ffind(self, text, word):
        i = 0
        while True:
            i = text.find(word, i)
            if i == -1:
                return
            end = i + len(word)
            yield i, end
            i += len(word)

    def find(self, word, source):
        self._text = source
        self._word = word
        self.start()