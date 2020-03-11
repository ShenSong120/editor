from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
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
        # self.search_line_edit.textChanged.connect(self.find_first_option)
        self.search_line_edit.textChanged.connect(self.search_line_edit_text_changed)
        self.search_line_edit.setStyleSheet('background-color:#000000; color:white;')
        self.search_line_edit.setMinimumWidth(200)
        self.search_line_edit.setMaximumWidth(400)
        # 搜索框内清除文本控件(点击清除文本)
        self.clear_search_edit_action = QAction(self.search_line_edit)
        self.clear_search_edit_action.setIcon(QIcon(Icon.clear_text))
        self.clear_search_edit_action.triggered.connect(self.clear_search_edit_text)
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
        # 是否区分大小写
        check_box_style = 'QCheckBox:indicator{background:transparent;border:1px solid #000000;width:18;height:18}\
                           QCheckBox::indicator:unchecked{image:url(' + Icon.unchecked + ')}\
                           QCheckBox::indicator:checked{image:url(' + Icon.checked + ')}'
        self.match_case_check_box = QCheckBox(self)
        self.match_case_check_box.setStyleSheet(check_box_style)
        self.match_case_check_box.stateChanged.connect(self.match_case_check_box_state_changed)
        self.match_case_label = QLabel(self)
        self.match_case_label.setText('区分大小写')
        # 大小写区分标志(默认不区分大小写)
        self.match_case_flag = False
        # 匹配数量
        self.match_num_label = QLabel(self)
        # 关闭按钮
        self.close_option_button = QToolButton(self)
        self.close_option_button.setToolTip('关闭搜索框')
        self.close_option_button.setStyleSheet('QToolButton{border-image: url(' + Icon.close + ')}')
        self.close_option_button.clicked.connect(self.close_option)
        # 搜索结果背景标记
        self.search_thread = SearchThread()
        self.search_thread.signal[str].connect(self.search_option_marker)
        # 搜索开始位置
        self.start_line = 0
        self.start_index = 0
        # 布局
        self.general_layout = QHBoxLayout(self)
        self.general_layout.setContentsMargins(0, 0, 5, 0)
        self.general_layout.setSpacing(0)
        self.general_layout.addWidget(self.search_line_edit)
        self.general_layout.addStretch(1)
        self.general_layout.addWidget(self.last_option_button)
        self.general_layout.addSpacing(20)
        self.general_layout.addWidget(self.next_option_button)
        self.general_layout.addStretch(1)
        self.general_layout.addWidget(self.match_case_check_box)
        self.general_layout.addWidget(self.match_case_label)
        self.general_layout.addStretch(1)
        self.general_layout.addWidget(self.match_num_label)
        self.general_layout.addStretch(6)
        self.general_layout.addWidget(self.close_option_button)
        self.general_layout.addSpacing(30)
        self.setLayout(self.general_layout)

    # 清除检索框文本
    def clear_search_edit_text(self):
        self.search_line_edit.clear()

    # 明确指标
    def clear_indicators(self, indicator):
        self.parentWidget().clearIndicatorRange(0, 0, self.parentWidget().lines(), 0, indicator)

    # 搜索结果北京标记
    def search_option_marker(self, signal_str):
        palabras = eval(signal_str)
        self.clear_indicators(self.parentWidget().WORD_INDICATOR)
        if len(palabras) == 0:
            self.parentWidget().fillIndicatorRange(0, 0, 0, 0, self.parentWidget().WORD_INDICATOR)
            char = 'No'
        else:
            for p in palabras:
                self.parentWidget().fillIndicatorRange(p[0], p[1], p[0], p[2], self.parentWidget().WORD_INDICATOR)
            char = str(len(palabras))
        self.match_num_label.setText(char+' matches')

    # 动态显示隐藏清除文本控件
    def search_line_edit_text_changed(self):
        if self.clear_search_edit_action in self.search_line_edit.actions():
            if self.search_line_edit.text() == '':
                self.search_line_edit.removeAction(self.clear_search_edit_action)
        else:
            if self.search_line_edit.text() != '':
                self.search_line_edit.addAction(self.clear_search_edit_action, QLineEdit.TrailingPosition)
        self.find_first_option()

    # 区分大小写check_box触发函数
    def match_case_check_box_state_changed(self):
        if self.match_case_check_box.checkState() == Qt.Checked:
            self.match_case_flag = True
        else:
            self.match_case_flag = False
        self.find_first_option()

    # QLineEdit控件中的查找当前匹配
    def find_first_option(self):
        text = self.search_line_edit.text()
        source_text = self.parentWidget().text()
        self.search_thread.find(text, source_text, self.match_case_flag)
        flag = self.parentWidget().findFirst(text, False, self.match_case_flag, False, False, True,
                                             self.start_line, self.start_index, True)
        if flag is False:
            self.parentWidget().setCursorPosition(self.start_line, self.start_index)

    # 查找上一个匹配(暂时不支持)
    def find_last_option(self):
        text = self.search_line_edit.text()
        self.parentWidget().findFirst(text, False, self.match_case_flag, False, True, False, -1, -1, True)
        self.parentWidget().findNext()

    # 查找下一个匹配
    def find_next_option(self):
        text = self.search_line_edit.text()
        self.parentWidget().findFirst(text, False, self.match_case_flag, False, True, True, -1, -1, True)
        self.get_current_position()

    # 关闭操作
    def close_option(self):
        self.setHidden(True)
        self.parentWidget().setCursorPosition(self.start_line, self.start_index)
        # 关闭搜索框后(清除搜索文本标记)
        self.search_option_marker('[]')

    # 获取当前光标位置
    def get_current_position(self):
        self.start_line, self.start_index = self.parentWidget().getCursorPosition()


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
            found_list = found_list
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

    def find(self, word, source, case_sensitive):
        if case_sensitive is False:
            self._text = source.lower()
            self._word = word.lower()
        else:
            self._text = source
            self._word = word
        self.start()