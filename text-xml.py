# coding:utf-8
import re
import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5.Qsci import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from threading import Thread

'''感谢https://blog.csdn.net/xiaoyangyang20/article/details/68923133?fps=1&locationNum=4
,https://blog.csdn.net/tgbus18990140382/article/details/26136661
,https://qscintilla.com
。'''


class MyQscintilla(QsciScintilla):
    def __init__(self, parent):
        super(MyQscintilla, self).__init__(parent)
        # 字体设置
        self.font = QFont()
        # font.setFamily('Courier')
        self.font.setFamily('Consolas')
        self.font.setPointSize(14)
        # 设置字体宽度相等
        self.font.setFixedPitch(True)
        self.setFont(self.font)
        self.setUtf8(True)
        self.setMarginsFont(self.font)
        self.setMarginWidth(0, 15)
        # 设置空格为点, \t为箭头
        # self.editor.setWhitespaceVisibility(QsciScintilla.WsVisible)
        # 设置换行符为(\r\n)
        self.setEolMode(QsciScintilla.EolWindows)
        # 设置换行符不可见
        self.setEolVisibility(False)
        # 设置空格点大小
        self.setWhitespaceSize(2)
        # 设置行号
        self.setMarginLineNumbers(0, True)
        # 文本编辑框中间有一条竖线
        # self.editor.setEdgeMode(QsciScintilla.EdgeLine)
        self.setEdgeColumn(80)
        self.setEdgeColor(QColor(0, 0, 0))
        # 设置光标宽度(0不显示光标)
        self.setCaretWidth(2)
        # 设置光标颜色
        self.setCaretForegroundColor(QColor('darkCyan'))
        # 高亮显示光标所在行
        self.setCaretLineVisible(True)
        # 选中行背景色
        self.setCaretLineBackgroundColor(QColor('#F0F0F0'))
        # 设置括号匹配(不设置)
        # self.setBraceMatching(QsciScintilla.StrictBraceMatch)
        # True:\t代表tab/False:\t代表空格
        self.setIndentationsUseTabs(True)
        # 如果在行首部空格位置tab，缩进的宽度字符数，并且不会转换为空格
        self.setIndentationWidth(0)
        # True:如果行前空格数少于tabwidth,补齐空格数, False:如果在文字前tab同true，如果在行首tab，则直接增加tabwidth个空格
        self.setTabIndents(True)
        # 换行后自动缩进
        self.setAutoIndent(True)
        self.setBackspaceUnindents(True)
        # tab宽度设置为8, 也就是四个字符
        self.setTabWidth(8)
        # 设置缩进的显示方式(用tab缩进时, 在缩进位置上显示一个竖点线)
        self.setIndentationGuides(True)
        # 设置折叠样式
        self.setFolding(QsciScintilla.PlainFoldStyle)
        # 设置折叠栏颜色
        self.setFoldMarginColors(Qt.gray, Qt.lightGray)
        # 设置2边栏宽度
        self.setMarginWidth(2, 12)
        self.markerDefine(QsciScintilla.Minus, QsciScintilla.SC_MARKNUM_FOLDEROPEN)
        self.markerDefine(QsciScintilla.Plus, QsciScintilla.SC_MARKNUM_FOLDER)
        self.markerDefine(QsciScintilla.Minus, QsciScintilla.SC_MARKNUM_FOLDEROPENMID)
        self.markerDefine(QsciScintilla.Plus, QsciScintilla.SC_MARKNUM_FOLDEREND)
        self.setMarkerBackgroundColor(QColor("#FFFFFF"), QsciScintilla.SC_MARKNUM_FOLDEREND)
        self.setMarkerForegroundColor(QColor("#272727"), QsciScintilla.SC_MARKNUM_FOLDEREND)
        self.setMarkerBackgroundColor(QColor("#FFFFFF"), QsciScintilla.SC_MARKNUM_FOLDEROPENMID)
        self.setMarkerForegroundColor(QColor("#272727"), QsciScintilla.SC_MARKNUM_FOLDEROPENMID)
        # 当前文档中出现的名称以及xml自带的都自动补全提示
        # self.setAutoCompletionSource(QsciScintilla.AcsDocument)
        self.setAutoCompletionSource(QsciScintilla.AcsAll)
        # 大小写敏感
        self.setAutoCompletionCaseSensitivity(True)
        # 是否用补全的字符串替换后面的字符串
        self.setAutoCompletionReplaceWord(False)
        # 输入一个字符就会出现自动补全的提示
        self.setAutoCompletionThreshold(1)
        self.setAutoCompletionUseSingle(QsciScintilla.AcusExplicit)
        self.autoCompleteFromAll()
        # 定义语言为xml语言
        self.lexer = QsciLexerXML(self)
        self.lexer.setDefaultFont(QFont('Consolas', 14))
        self.setLexer(self.lexer)
        self.__api = QsciAPIs(self.lexer)
        auto_completions = ['note', 'shen', 'song']
        for ac in auto_completions:
            self.__api.add(ac)
        self.__api.prepare()
        # 触发事件
        self.old_text = ''
        # self.textChanged.connect(self.changed)
        self.cursorPositionChanged.connect(self.cursor_move)

    def changed(self):
        line_digit = len(str(len(self.text().split('\n'))))
        margin_width = 15 + (line_digit - 1) * 10
        self.setMarginWidth(0, margin_width)
        # 文本内容
        text = self.text()
        # 只有新增字符的情况下才允许自动补全
        if len(text) > len(self.old_text):
            line, index = self.getCursorPosition()
            self.setSelection(line, index, line, index+1)
            print(self.selectedText())
            self.replaceSelectedText('<>')
            # self.insertAt('<>', line, index + 1)
        else:
            pass
        self.old_text = text
        # Thread(target=self.complete_other, args=()).start()

    # 光标移动事件
    def cursor_move(self):
        # 调整边栏宽度
        line_digit = len(str(len(self.text().split('\n'))))
        margin_width = 15 + (line_digit - 1) * 10
        self.setMarginWidth(0, margin_width)
        # 文本内容
        text = self.text()
        # 只有新增字符的情况下才允许自动补全
        if len(text) > len(self.old_text):
            line, index = self.getCursorPosition()
            if list(text)[index-1] == '>':
                print(line, index)
            # self.setSelection(line, index-1, line, index)
            # print(self.selectedText())
            # self.insertAt('<>', line, index)
        else:
            pass
        self.old_text = text

    def complete_other(self):
        # 文本内容
        text = self.text()
        line, index = self.getCursorPosition()
        # 只有新增字符的情况下才允许自动补全
        if len(text) > len(self.old_text):
            index += 1
            current_line_text = self.text(line)
            list_current_line_text = list(current_line_text)
            if list_current_line_text[index-1] == '>':
                other_text = re.findall("<.+?>", ''.join(current_line_text[:index]))[0]
                print(other_text)
                self.insertAt(other_text, line, 0)
        else:
            pass
        self.old_text = text

    # 切换注释
    def toggle_comment(self):
        # 是否需要注释的标志
        comment_line_num = 0
        # 获取起始和结束行号
        start_line, end_line = self.get_selections()
        for line in range(start_line, end_line + 1):
            current_line_text = self.text(line).strip()
            if current_line_text.startswith('<!--') and current_line_text.endswith('-->'):
                comment_line_num = comment_line_num
            else:
                comment_line_num += 1
        if comment_line_num > 0:
            # 添加注释
            self.add_comment(start_line, end_line)
        else:
            # 取消注释
            self.cancel_comment(start_line, end_line)

    # 获取选中行(注释需要用到, 开始行和结束行)
    def get_selections(self):
        start_position = self.SendScintilla(QsciScintillaBase.SCI_GETSELECTIONSTART)
        end_position = self.SendScintilla(QsciScintillaBase.SCI_GETSELECTIONEND)
        start_line = self.SendScintilla(QsciScintillaBase.SCI_LINEFROMPOSITION, start_position)
        end_line = self.SendScintilla(QsciScintillaBase.SCI_LINEFROMPOSITION, end_position)
        return start_line, end_line

    # 添加注释
    def add_comment(self, start_line, end_line):
        last_line = end_line
        # 如果选中的最后一行是整个文本的最后一行
        if last_line == self.lines() - 1:
            end_index = len(self.text(end_line))
        else:
            end_index = len(self.text(end_line)) - 1
        # 设置选中(开始行/列, 结束行/列)
        self.setSelection(start_line, 0, end_line, end_index)
        selected_text = self.selectedText()
        selected_list = selected_text.split('\r\n')
        indent_position = []
        for line in selected_list:
            if line:
                indent_position.append(len(line) - len(line.lstrip()))
        for i, line in enumerate(selected_list):
            if line.strip() != '':
                selected_list[i] = line[:indent_position[i]] + '<!-- ' + line[indent_position[i]:] + ' -->'
            else:
                selected_list[i] = line
        replace_text = '\r\n'.join(selected_list)
        self.replaceSelectedText(replace_text)

    # 取消注释
    def cancel_comment(self, start_line, end_line):
        last_line = end_line
        # 如果选中的最后一行是整个文本的最后一行
        if last_line == self.lines() - 1:
            end_index = len(self.text(end_line))
        else:
            end_index = len(self.text(end_line)) - 1
        # 设置选中(开始行/列, 结束行/列)
        self.setSelection(start_line, 0, end_line, end_index)
        selected_text = self.selectedText()
        selected_list = selected_text.split('\r\n')
        indent_position = []
        for line in selected_list:
            if line:
                indent_position.append(len(line) - len(line.lstrip()))
        for i, line in enumerate(selected_list):
            if line.strip() != '':
                selected_list[i] = line.replace('<!-- ', '', 1).replace(' -->', '', 1)
            else:
                selected_list[i] = line
        replace_text = '\r\n'.join(selected_list)
        self.replaceSelectedText(replace_text)

    # 这是重写键盘事件
    def keyPressEvent(self, event):
        # Ctrl + / 键 注释or取消注释
        if (event.key() == Qt.Key_Slash):
            if QApplication.keyboardModifiers() == Qt.ControlModifier:
                # 切换注释
                self.toggle_comment()
            else:
                # 不要破坏原有功能
                QsciScintilla.keyPressEvent(self, event)
        else:
            # 不要破坏原有功能
            QsciScintilla.keyPressEvent(self, event)

    # 鼠标滚动事件(字体放大缩小)
    def wheelEvent(self, event):
        # Ctrl + 滚轮 控制字体缩放
        if QApplication.keyboardModifiers() == Qt.ControlModifier:
            da = event.angleDelta()
            # QsciScintilla 自带缩放的功能, 参数是增加的字体点数
            if da.y() > 0:
                self.zoomIn(1)
            elif da.y() < 0:
                self.zoomOut(1)
        else:
            super().wheelEvent(event)   # 留点汤给父类，不然滚轮无法翻页


class MainWindow(QMainWindow):
    def __init__(self, parent=None, title='未命名'):
        super(MainWindow, self).__init__(parent)
        self.setGeometry(100, 100, 1000, 700)
        self.setWindowTitle(title)
        # 字体设置
        font = QFont()
        # font.setFamily('Courier')
        font.setFamily('Consolas')
        font.setPointSize(14)
        # 设置字体宽度相等
        font.setFixedPitch(True)
        self.setFont(font)
        # 编辑器设置
        self.editor = MyQscintilla(self)
        self.setCentralWidget(self.editor)


def main():
    app = QApplication(sys.argv)
    form = MainWindow(None, 'xml-editor')
    form.show()
    app.exec_()


main()
