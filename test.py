# coding:utf-8
import re
import os
import sys
import time
import shutil
import configparser
from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5.Qsci import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from threading import Thread
from glv import Icon, MergePath

'''
需要增加的功能:
1.块导入
2.点击跳转
'''


class MyLexerXML(QsciLexerXML):
    def __init__(self, parent):
        super(MyLexerXML, self).__init__(parent)
        # 设置标签大小写不敏感
        self.setCaseSensitiveTags(False)
        # 设置自动缩进样式
        self.setAutoIndentStyle(QsciScintilla.AiMaintain)
        # self.setAutoIndentStyle(QsciScintilla.AiOpening)
        # self.setAutoIndentStyle(QsciScintilla.AiClosing)



class MyQscintilla(QsciScintilla):
    signal = pyqtSignal(str)

    def __init__(self, parent, file=None):
        super(MyQscintilla, self).__init__(parent)
        self.font = QFont('Consolas', 14, QFont.Bold)
        # self.font = QFont('Ubuntu Mono', 14)
        # self.font = QFont('Arial ', 14)
        self.setFont(self.font)
        self.setUtf8(True)
        # self.setMarginsFont(self.font)
        self.setMarginsFont(QFont('Arial ', 14))
        self.setMarginWidth(0, 20)
        # 设置行号
        self.setMarginLineNumbers(0, True)
        # 设置换行符为(\r\n)
        self.setEolMode(QsciScintilla.EolWindows)
        # 设置光标宽度(0不显示光标)
        self.setCaretWidth(2)
        # 设置光标颜色
        self.setCaretForegroundColor(QColor('darkCyan'))
        # 高亮显示光标所在行
        self.setCaretLineVisible(True)
        # 选中行背景色
        self.setCaretLineBackgroundColor(QColor('#F0F0F0'))
        # tab宽度设置为8, 也就是四个字符
        self.setTabWidth(4)
        # 换行后自动缩进
        self.setAutoIndent(True)
        self.setBackspaceUnindents(True)
        # 设置缩进的显示方式(用tab缩进时, 在缩进位置上显示一个竖点线)
        self.setIndentationGuides(True)
        # 设置折叠样式
        self.setFolding(QsciScintilla.PlainFoldStyle)
        # 设置折叠栏颜色
        self.setFoldMarginColors(Qt.gray, Qt.lightGray)
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
        # self.setAutoCompletionUseSingle(QsciScintilla.AcusAlways)
        self.autoCompleteFromAll()
        # 右键菜单
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_menu)
        # 保存每一次操作后的text
        self.old_text = ''
        # 触发事件
        self.cursorPositionChanged.connect(self.cursor_move)
        # 提示框选项图标(单词和函数的区分)
        word_image = QPixmap(Icon.word)
        function_image = QPixmap(Icon.function)
        self.registerImage(1, word_image)
        self.registerImage(2, function_image)
        # 获取配置文件
        self.cf = configparser.ConfigParser()
        self.cf.read('config.ini', encoding='utf-8')
        self.begin_line_label = self.cf.get('begin_line', 'label')
        self.key_words = eval(self.cf.get('keywords', 'word_list'))
        self.function_dict = {}
        for key in self.cf.options('function'):
            function = str(self.cf.get('function', key))
            function = function.replace('\\r', '\r')
            function = function.replace('\\n', '\n')
            function = function.replace('\\t', '\t')
            self.function_dict[key] = function
        # 定义语言为xml语言
        # self.lexer = QsciLexerXML(self)
        self.lexer = MyLexerXML(self)
        # self.lexer.setDefaultFont(self.font)
        self.lexer.setFont(self.font)
        self.setLexer(self.lexer)
        self.__api = QsciAPIs(self.lexer)
        auto_completions = self.key_words + list(self.function_dict.keys())
        for item in auto_completions:
            # 如果是函数(图标显示function)
            if item in list(self.function_dict.keys()):
                auto_completions[auto_completions.index(item)] = item + '?2'
            # 如果是单词(图标显示word)
            else:
                auto_completions[auto_completions.index(item)] = item + '?1'
        for ac in auto_completions:
            self.__api.add(ac)
        self.__api.prepare()
        # 新建文件还是导入文件
        if file is None:
            # 默认第一行内容
            self.setText(self.begin_line_label)
        else:
            with open(file, 'r', encoding='utf-8') as f:
                editor_text = f.read()
            self.setText(editor_text)

    # 右键菜单展示
    def show_menu(self, point):
        # 菜单样式(整体背景#4D4D4D,选中背景#1E90FF,选中字体#E8E8E8,选中边界#575757,分离器背景#757575)
        menu_qss = "QMenu{color: #242424; background: #F0F0F0; margin: 2px;}\
                    QMenu::item{padding:3px 20px 3px 20px;}\
                    QMenu::indicator{width:13px; height:13px;}\
                    QMenu::item:selected:enabled{color:#242424; border:0px solid #575757; background:#1E90FF;}\
                    QMenu::item:selected:!enabled{color:#969696; border:0px solid #575757; background:#99CCFF;}\
                    QMenu::item:!enabled{color: #969696;}\
                    QMenu::item:enabled{color: #242424;}\
                    QMenu::separator{height:1px; background:#757575;}"
        self.menu = QMenu(self)
        self.menu.setStyleSheet(menu_qss)
        # 撤销上一操作
        self.undo_action = QAction('撤消上一次操作(Ctrl+Z)', self)
        self.undo_action.triggered.connect(self.undo_operate)
        if self.isUndoAvailable() is False:
            self.undo_action.setEnabled(False)
        # 恢复上一操作
        self.redo_action = QAction('恢复上一次操作(Ctrl+Y)', self)
        self.redo_action.triggered.connect(self.redo_operate)
        if self.isRedoAvailable() is False:
            self.redo_action.setEnabled(False)
        # 剪切
        self.cut_action = QAction('剪切(Ctrl+X)', self)
        self.cut_action.triggered.connect(self.cut_operate)
        if self.selectedText() == '':
            self.cut_action.setEnabled(False)
        # 复制
        self.copy_action = QAction('复制(Ctrl+C)', self)
        self.copy_action.triggered.connect(self.copy_operate)
        if self.selectedText() == '':
            self.copy_action.setEnabled(False)
        # 粘贴
        self.paste_action = QAction('粘贴(Ctrl+V)', self)
        self.paste_action.triggered.connect(self.paste_operate)
        # 删除
        self.delete_action = QAction('删除', self)
        self.delete_action.triggered.connect(self.delete_operate)
        if self.selectedText() == '':
            self.delete_action.setEnabled(False)
        # 全部选中
        self.select_all_action = QAction('选中全部(Ctrl+A)', self)
        self.select_all_action.triggered.connect(self.select_all_operate)
        # 添加/去除-注释
        self.comment_action = QAction('添加/去除-注释(Ctrl+L)', self)
        self.comment_action.triggered.connect(self.comment_operate)
        # 菜单添加action
        self.menu.addAction(self.undo_action)
        self.menu.addAction(self.redo_action)
        self.menu.addAction(self.cut_action)
        self.menu.addAction(self.copy_action)
        self.menu.addAction(self.paste_action)
        self.menu.addAction(self.delete_action)
        self.menu.addAction(self.select_all_action)
        self.menu.addAction(self.comment_action)
        self.menu.exec(self.mapToGlobal(point))

    def undo_operate(self):
        # 注释的时候先关闭自动补全后半部分功能
        self.cursorPositionChanged.disconnect(self.cursor_move)
        # 切换注释
        self.undo()
        self.cursorPositionChanged.connect(self.cursor_move)
        self.old_text = self.text()

    def redo_operate(self):
        # 注释的时候先关闭自动补全后半部分功能
        self.cursorPositionChanged.disconnect(self.cursor_move)
        # 切换注释
        self.redo()
        self.cursorPositionChanged.connect(self.cursor_move)
        self.old_text = self.text()

    def cut_operate(self):
        # 注释的时候先关闭自动补全后半部分功能
        self.cursorPositionChanged.disconnect(self.cursor_move)
        # 切换注释
        self.cut()
        self.cursorPositionChanged.connect(self.cursor_move)
        self.old_text = self.text()

    def copy_operate(self):
        # 注释的时候先关闭自动补全后半部分功能
        self.cursorPositionChanged.disconnect(self.cursor_move)
        # 切换注释
        self.copy()
        self.cursorPositionChanged.connect(self.cursor_move)
        self.old_text = self.text()

    def paste_operate(self):
        # 注释的时候先关闭自动补全后半部分功能
        self.cursorPositionChanged.disconnect(self.cursor_move)
        # 切换注释
        self.paste()
        self.cursorPositionChanged.connect(self.cursor_move)
        self.old_text = self.text()

    def delete_operate(self):
        # 注释的时候先关闭自动补全后半部分功能
        self.cursorPositionChanged.disconnect(self.cursor_move)
        # 切换注释
        self.removeSelectedText()
        self.cursorPositionChanged.connect(self.cursor_move)
        self.old_text = self.text()

    def select_all_operate(self):
        # 注释的时候先关闭自动补全后半部分功能
        self.cursorPositionChanged.disconnect(self.cursor_move)
        # 切换注释
        self.selectAll(True)
        self.cursorPositionChanged.connect(self.cursor_move)
        self.old_text = self.text()

    def comment_operate(self):
        # 注释的时候先关闭自动补全后半部分功能
        self.cursorPositionChanged.disconnect(self.cursor_move)
        # 切换注释
        self.toggle_comment()
        self.cursorPositionChanged.connect(self.cursor_move)
        self.old_text = self.text()

    # 光标移动事件
    def cursor_move(self):
        # 调整边栏宽度
        line_digit = len(str(len(self.text().split('\n'))))
        margin_width = 20 + (line_digit - 1) * 13
        self.setMarginWidth(0, margin_width)
        # 文本内容
        text = self.text()
        # 当前文本长度和上次文本长度
        text_length = len(text)
        old_text_length = len(self.old_text)
        line, index = self.getCursorPosition()
        # 只有新增字符的情况下才执行如下代码(删除文本不需要执行)
        if text_length > old_text_length:
            # 通过键盘键入字符
            if (text_length - old_text_length) == 1:
                # line, index = self.getCursorPosition()
                current_line_text = self.text(line)
                list_current_line_text = list(current_line_text)
                current_char = list_current_line_text[index-1] if index > 0 else None
                if current_char == '>':
                    for i in range(index-1, -1, -1):
                        if list_current_line_text[i] == '<' and list_current_line_text[i+1] != '?':
                            key_words = ''.join(list_current_line_text[i+1:index-1])
                            self.insertAt('</'+key_words+'>', line, index)
                            break
        self.old_text = self.text()
        # 获取当前光标
        cursor_position = '[' + str(line) + ':' + str(index) + ']'
        self.signal.emit('cursor_position>' + cursor_position)

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
        if len(selected_list) > 1 and selected_list[-1] == '':
            selected_list.pop(-1)
        # 保存将每一行切为的三个部分(三个部分为一个list)
        line_separate_list = []
        # 注释结束后光标位置(默认-1,此时不需要设置光标位置)
        cursor_position = -1
        # 将一行内容拆解三个部分(1\t or '' 2<note> 3 ''or...)
        for line in selected_list:
            # 如果存在line内容
            if line:
                line_list = []
                if '<' in line and '>' in line:
                    line_list.append(line.split('<')[0])
                    line_list.append(re.findall('<.*>', line)[0])
                    line_list.append(line.split('>')[-1])
                    line_separate_list.append(line_list)
                elif len(line) > 0:
                    line_list.append(re.findall('\s*', line)[0])
                    line_list.append(line.strip())
                    line_list.append('')
                    line_separate_list.append(line_list)
                    if line.strip() == '':
                        cursor_position = len(line) + 4
                else:
                    line_list = ['', '', '']
                    line_separate_list.append(line_list)
                    cursor_position =  4
            else:
                line_list = ['', '', '']
                line_separate_list.append(line_list)
                cursor_position = 4
        for i in range(len(line_separate_list)):
            if '<!--' not in selected_list[i] and '-->' not in selected_list[i]:
                selected_list[i] = line_separate_list[i][0] + '<!--' + line_separate_list[i][1] + '-->' + line_separate_list[i][2]
        if self.text(end_line).endswith('\r\n'):
            replace_text = '\r\n'.join(selected_list) + '\r\n'
        else:
            replace_text = '\r\n'.join(selected_list)
        self.replaceSelectedText(replace_text)
        if cursor_position != -1:
            self.setCursorPosition(end_line, cursor_position)

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
        for line in selected_list:
            if '<!--' in line and '-->' in line:
                selected_list[selected_list.index(line)] = line.replace('<!--', '', 1).replace('-->', '', 1)
        replace_text = '\r\n'.join(selected_list)
        self.replaceSelectedText(replace_text)

    # 删除单/双引号操作
    def delete_quotation_marks(self, event):
        line, index = self.getCursorPosition()
        current_line_text = self.text(line)
        current_line_text_list = list(current_line_text)
        # 当前光标肯定不是行末('')
        if len(current_line_text) > index:
            current_char = current_line_text_list[index-1]
            next_char = current_line_text_list[index]
            if current_char == next_char and current_char in ["'", '"']:
                self.setSelection(line, index-1, line, index+1)
                self.replaceSelectedText('')
            else:
                # 不要破坏原有功能
                QsciScintilla.keyPressEvent(self, event)
        else:
            # 不要破坏原有功能
            QsciScintilla.keyPressEvent(self, event)

    # 敲回车自动补全处理函数
    def auto_completion(self, event):
        line_before, index_before = self.getCursorPosition()
        QsciScintilla.keyPressEvent(self, event)
        line_after, index_after = self.getCursorPosition()
        # 获取当前鼠标位置单词(此处可以重新获取这个词,只以空格为分割)
        current_word = self.wordAtLineIndex(line_after, index_after)
        if current_word != '':
            print('自动补全: ', current_word)
            # 选中补全的单词(后面会用段落代替)
            self.setSelection(line_after, index_after-len(current_word), line_after, index_after)
            # 替换为函数块
            if current_word in self.function_dict.keys():
                self.replaceSelectedText(self.function_dict[current_word])
            else:
                # 此处可以添加更改(将函数名代替为函数)
                self.setCursorPosition(line_after, index_after)

    # 这是重写键盘事件
    def keyPressEvent(self, event):
        # Ctrl + / 键 注释or取消注释
        if (event.key() == Qt.Key_Slash):
            if QApplication.keyboardModifiers() == Qt.ControlModifier:
                self.comment_operate()
            else:
                # 不要破坏原有功能
                QsciScintilla.keyPressEvent(self, event)
        # Ctrl + Z 键 撤销上一步操作
        elif (event.key() == Qt.Key_Z):
            if QApplication.keyboardModifiers() == Qt.ControlModifier:
                self.undo_operate()
            else:
                # 不要破坏原有功能
                QsciScintilla.keyPressEvent(self, event)
        # Ctrl + Y 键 恢复上一步操作
        elif (event.key() == Qt.Key_Y):
            if QApplication.keyboardModifiers() == Qt.ControlModifier:
                self.redo_operate()
            else:
                # 不要破坏原有功能
                QsciScintilla.keyPressEvent(self, event)
        # Ctrl + X 键 剪切
        elif (event.key() == Qt.Key_X):
            if QApplication.keyboardModifiers() == Qt.ControlModifier:
                self.cut_operate()
            else:
                # 不要破坏原有功能
                QsciScintilla.keyPressEvent(self, event)
        # Ctrl + C 键 复制
        elif (event.key() == Qt.Key_C):
            if QApplication.keyboardModifiers() == Qt.ControlModifier:
                self.copy_operate()
            else:
                # 不要破坏原有功能
                QsciScintilla.keyPressEvent(self, event)
        # Ctrl + V 键 粘贴
        elif (event.key() == Qt.Key_V):
            if QApplication.keyboardModifiers() == Qt.ControlModifier:
                self.paste_operate()
            else:
                # 不要破坏原有功能
                QsciScintilla.keyPressEvent(self, event)
        # Ctrl + A 键 全部选中
        elif (event.key() == Qt.Key_A):
            if QApplication.keyboardModifiers() == Qt.ControlModifier:
                self.select_all_operate()
            else:
                # 不要破坏原有功能
                QsciScintilla.keyPressEvent(self, event)
        # Ctrl + D 键(需要更新old_text)
        elif (event.key() == Qt.Key_D):
            if QApplication.keyboardModifiers() == Qt.ControlModifier:
                # 不要破坏原有功能
                QsciScintilla.keyPressEvent(self, event)
                self.old_text = self.text()
            else:
                # 不要破坏原有功能
                QsciScintilla.keyPressEvent(self, event)
        # 单引号处理
        elif (event.key() == Qt.Key_Apostrophe):
            QsciScintilla.keyPressEvent(self, event)
            self.insert("'")
            self.old_text = self.text()
        # 双引号处理
        elif (event.key() == Qt.Key_QuoteDbl):
            QsciScintilla.keyPressEvent(self, event)
            self.insert('"')
            self.old_text = self.text()
        # 删除单/双引号处理
        elif (event.key() == Qt.Key_Backspace):
            self.delete_quotation_marks(event)
            self.old_text = self.text()
        # 回车自动补全处理
        elif (event.key() == Qt.Key_Return):
            self.auto_completion(event)
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

# 侧边工程栏
class ProjectBar(QWidget):

    signal = pyqtSignal(str)

    def __init__(self, parent, path):
        super(ProjectBar, self).__init__(parent)
        # 设置工程栏背景颜色
        self.setStyleSheet('background-color: #F0F0F0;')
        self.parent = parent
        self.path = path
        # 文件模型
        self.model = QFileSystemModel(self)
        # 改表头名字(无效)
        # self.model.setHeaderData(0, Qt.Horizontal, "123455")
        # 文件过滤
        # self.model.setFilter(QDir.NoDotAndDotDot | QDir.AllDirs)
        # 需要显示的文件
        # filters = ['*.mp4', '*.avi', '*.mov', '*.flv', '*.html', '*.jpg', '*.png', '*.xls', '*.xlsx', '*.xml', '*.txt', '*.ini']
        filters = ['*']
        self.model.setRootPath(self.path)
        self.model.setNameFilters(filters)
        self.model.setNameFilterDisables(False)
        # 树形视图
        self.tree = QTreeView(self)  # 2
        # 右键菜单
        self.tree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree.customContextMenuRequested.connect(self.show_menu)
        self.tree.setModel(self.model)
        # 后面的size/type/data不显示
        self.tree.setColumnHidden(1, True)
        self.tree.setColumnHidden(2, True)
        self.tree.setColumnHidden(3, True)
        self.tree.setHeaderHidden(True)
        self.tree.setRootIndex(self.model.index(self.path))
        self.tree.clicked.connect(self.show_info)
        self.tree.doubleClicked.connect(lambda : self.operation_file(None))
        # 工程栏路径信息展示
        self.info_label = QLineEdit(self)
        self.info_label.setReadOnly(True)
        self.info_label.setText(self.path)
        # 总体布局
        self.v_layout = QVBoxLayout()
        self.v_layout.setContentsMargins(0, 0, 0, 0)
        self.v_layout.setSpacing(0)
        self.v_layout.addWidget(self.info_label)
        self.v_layout.addWidget(self.tree)
        self.setLayout(self.v_layout)

    def show_menu(self, point):
        index = self.tree.indexAt(point)
        # 如果点击的非空白区域
        if index.isValid():
            # 当前节点路径以及名字
            # index = self.tree.currentIndex()
            node_name = self.model.fileName(index)
            node_path = self.model.filePath(index)
            blank_click_flag = False
        # 点击空白区域
        else:
            self.tree.clearSelection()
            node_name = os.path.split(self.path)[1]
            node_path = self.path
            blank_click_flag = True
        # 更新显示标签
        self.info_label.setText(node_path)
        # 菜单样式
        menu_qss = "QMenu{color: #E8E8E8; background: #4D4D4D; margin: 2px;}\
                    QMenu::item{padding:3px 20px 3px 20px;}\
                    QMenu::indicator{width:13px; height:13px;}\
                    QMenu::item:selected{color:#E8E8E8; border:0px solid #575757; background:#1E90FF;}\
                    QMenu::separator{height:1px; background:#757575;}"
        self.menu = QMenu(self)
        self.menu.setStyleSheet(menu_qss)
        # 新建文件
        self.new_file_action = QAction('新建文件', self)
        self.new_file_action.triggered.connect(lambda : self.new_file_dialog(index, node_path, blank_click_flag))
        # 新建文件夹
        self.new_folder_action = QAction('新建文件夹', self)
        self.new_folder_action.triggered.connect(lambda : self.new_folder_dialog(index, node_path, blank_click_flag))
        # 重命名
        self.rename_action = QAction('重命名', self)
        self.rename_action.triggered.connect(lambda : self.rename_dialog(node_path, node_name, blank_click_flag))
        # 删除
        self.delete_action = QAction('删除', self)
        self.delete_action.triggered.connect(lambda : self.delete_dialog(node_path, blank_click_flag))
        # 菜单添加action
        self.menu.addAction(self.new_file_action)
        self.menu.addAction(self.new_folder_action)
        self.menu.addAction(self.rename_action)
        self.menu.addAction(self.delete_action)
        self.menu.exec(self.tree.mapToGlobal(point))

    # 新建文件
    def new_file_dialog(self, index, node_path, blank_click_flag):
        title, prompt_text, default_name = '新建文件', '请输入文件名', ''
        file_name, ok = QInputDialog.getText(self, title, prompt_text, QLineEdit.Normal, default_name)
        if ok:
            if os.path.isdir(node_path) is True:
                root_path = node_path
                # 展开文件夹
                self.tree.setExpanded(index, True)
            else:
                root_path = os.path.dirname(node_path)
            file_path = MergePath(root_path, file_name).merged_path
            f = open(file_path, 'w', encoding='utf-8')
            f.close()
            print('新建文件: %s' % file_path)
            # 判断是否在空白区域
            if blank_click_flag is True:
                # index = self.model.index(QDir.currentPath())
                # index = self.model.index(file_path)
                Thread(target=self.update_select_item, args=(file_path,)).start()
            else:
                # 更新选中item
                Thread(target=self.update_select_item, args=(file_path,)).start()

    # 新建文件夹
    def new_folder_dialog(self, index, node_path, blank_click_flag):
        title, prompt_text, default_name = '新建文件夹', '请输入文件夹名', ''
        folder_name, ok = QInputDialog.getText(self, title, prompt_text, QLineEdit.Normal, default_name)
        if ok:
            if os.path.isdir(node_path) is True:
                root_path = node_path
                # 展开文件夹
                self.tree.setExpanded(index, True)
            else:
                root_path = os.path.dirname(node_path)
            folder_path = MergePath(root_path, folder_name).merged_path
            os.makedirs(folder_path)
            print('新建文件夹: %s' % folder_path)
            # 判断是否在空白区域
            if blank_click_flag is True:
                # index = self.model.index(QDir.currentPath())
                Thread(target=self.update_select_item, args=(folder_path,)).start()
            else:
                # 更新选中item
                Thread(target=self.update_select_item, args=(folder_path,)).start()


    # 重命名
    def rename_dialog(self, node_path, node_name, blank_click_flag):
        if blank_click_flag is True:
            return
        title, prompt_text, default_name = '重命名', '请输入新文件名', node_name
        new_name, ok = QInputDialog.getText(self, title, prompt_text, QLineEdit.Normal, default_name)
        if ok:
            root_path = os.path.dirname(node_path)
            new_name_path = MergePath(root_path, new_name).merged_path
            os.rename(node_path, new_name_path)
            print('重命名 %s 为: %s' % (node_path, new_name_path))
            Thread(target=self.update_select_item, args=(new_name_path,)).start()


    # 删除文件
    def delete_dialog(self, node_path, blank_click_flag):
        if blank_click_flag is True:
            return
        # file_flag判断是文件还是文件夹(文件为True,文件夹为False)
        if os.path.isdir(node_path) is True:
            file_flag = False
            prompt_text = '确定要删除此文件夹吗？'
        else:
            file_flag = True
            prompt_text = '确定要删除此文件吗？'
        # 判断是否确定删除
        reply = QMessageBox.question(self, '删除栏', prompt_text, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            # 获取删除项下一项名字
            name = self.tree.indexBelow(self.model.index(node_path)).data()
            parent_path = os.path.split(node_path)[0]
            # 确保路径存在
            selected_path = parent_path if name is None else MergePath(parent_path, name).merged_path
            if os.path.exists(selected_path) is False:
                selected_path = parent_path
            Thread(target=self.update_select_item, args=(selected_path,)).start()
            self.info_label.setText(selected_path)
            if file_flag is True:
                os.remove(node_path)
                print('删除文件: %s' % node_path)
            else:
                shutil.rmtree(node_path)
                print('删除文件夹: %s' % node_path)

    # 更新选中item(必须异步线程才能选中, 也就是等待文件model更新完成, 延时时间不能太短)
    def update_select_item(self, path):
        time.sleep(0.04)
        new_index = self.model.index(path)
        self.tree.setCurrentIndex(new_index)
        self.info_label.setText(path)

    # 更新文件名字显示
    def show_info(self):  # 4
        index = self.tree.currentIndex()
        if index.isValid():
            file_name = self.model.fileName(index)
            file_path = self.model.filePath(index)
            self.info_label.setText(file_path)

    # 双击操作
    def operation_file(self, file_path=None):
        if file_path is None:
            index = self.tree.currentIndex()
            file_path = self.model.filePath(index)
        else:
            file_path = file_path
        # 判断双击是否为文件(只对文件操作)
        if os.path.isfile(file_path) is True:
            # 展示图片
            if file_path.endswith('.jpg') or file_path.endswith('.png') or file_path.endswith('.bmp'):
                self.signal.emit('open_picture>' + str(file_path))
            # 展示报告
            elif file_path.endswith('.html'):
                self.signal.emit('open_report>' + str(file_path))
            # 展示text
            elif file_path.split('.')[1] in ['txt', 'py', 'xml', 'md', 'ini']:
                self.signal.emit('open_text>' + str(file_path))
            # 播放视频
            elif file_path.split('.')[1] in ['mp4', 'MP4', 'avi', 'AVI', 'mov', 'MOV', 'flv', 'FLV']:
                self.signal.emit('open_video>' + str(file_path))
            # 展示excel文件
            elif file_path.split('.')[1] in ['xls', 'xlsx', 'XLS', 'XLSX']:
                self.signal.emit('open_excel>' + str(file_path))
            else:
                print('暂不支持此类型文件!!!')
        else:
            pass

# 编辑器分页器
class EditWidget(QTabWidget):

    signal = pyqtSignal(str)

    def __init__(self, parent):
        super(EditWidget, self).__init__(parent)
        self.parent = parent
        # 打开的文件列表(第一个默认视频tab)
        self.file_list = ['new.xml']
        # 存储新建文件name(如new.xml, new1.xml)
        self.new_file_list = ['new.xml']
        # 设置tab可以关闭
        self.setTabsClosable(True)
        # 样式设置
        style_sheet = 'QTabWidget:pane{ border: 1px solid #7A7A7A; top: -1px;}\
                       QTabWidget:tab-bar{border: 1px solid blue; top: 0px; alignment:left; background: blue}\
                       QTabBar::tab{height: 23px; margin-right: 0px; margin-bottom:-3px; padding-left: 5px; padding-right: 5px;}\
                       QTabBar::tab:selected{border: 1px solid #0099FF; color: #0099FF; background-color: white; border-top: 1px solid #0099FF; border-bottom: 5px solid #0099FF;}\
                       QTabBar::tab:!selected{border: 1px solid #7A7A7A;}\
                       QTabBar::tab:!selected:hover{border: 1px solid #7A7A7A; color: #0099CC;}\
                       QTabBar::close-button {image: url(' + Icon.close_tab + '); subcontrol-position: bottom right;}\
                       QTabBar::close-button:hover {image: url(' + Icon.close_tab_hover + ');}'
        self.setStyleSheet(style_sheet)
        # 切换tab事件
        self.currentChanged.connect(self.switch_tab)
        # 关闭tab触发事件
        self.tabCloseRequested.connect(self.close_tab)
        # 标签位置放在底部
        # self.setTabPosition(self.South)
        # 设置某一栏不可关闭
        # self.tabBar().setTabButton(0, QTabBar.RightSide, None)
        # tab_bar不自动隐藏
        self.tabBar().setAutoHide(False)
        # 默认打开一个新文件
        editor = MyQscintilla(self)
        editor.signal[str].connect(self.get_editor_signal)
        self.addTab(editor, 'new.xml')
        self.setTabToolTip(0, 'new.xml')

    # 新建文件
    def new_edit_tab(self):
        if None not in self.new_file_list:
            # 新增占位符
            self.new_file_list.append(None)
        tab_name = 'new.xml'
        for index in range(len(self.new_file_list)):
            if self.new_file_list[index] is None:
                if index > 0:
                    tab_name = 'new' + str(index) + '.xml'
                    self.new_file_list[index] = tab_name
                break
        self.file_list.append(tab_name)
        editor = MyQscintilla(self)
        editor.signal[str].connect(self.get_editor_signal)
        self.addTab(editor, tab_name)
        self.setCurrentWidget(editor)
        index = self.indexOf(editor)
        self.setTabToolTip(index, tab_name)

    # 打开文件
    def open_edit_tab(self):
        file, file_type = QFileDialog.getOpenFileName(self, "选取文件", "./", "Xml Files (*.xml)", options=QFileDialog.DontUseNativeDialog) # 设置文件扩展名过滤,注意用双分号间隔
        if file:
            self.file_list.append(file)
            tab_name = os.path.split(file)[1]
            editor = MyQscintilla(self, file=file)
            editor.signal[str].connect(self.get_editor_signal)
            self.addTab(editor, tab_name)
            self.setCurrentWidget(editor)
            index = self.indexOf(editor)
            self.setTabToolTip(index, file)

    # 保存文件
    def save_edit_tab(self):
        index = self.currentIndex()
        editor = self.currentWidget()
        file = str(self.file_list[index])
        if os.path.exists(file):
            with open(file, 'w+', encoding='utf-8') as f:
                f.write(editor.text())
            return True
        else:
            file_name, file_type = QFileDialog.getSaveFileName(self, '保存文件', './', 'Xml file(*.xml)', options=QFileDialog.DontUseNativeDialog)
            if file_name:
                with open(file_name, 'w+', encoding='utf-8') as f:
                    f.write(editor.text())
                self.file_list[index] = file_name
                tab_name = os.path.split(file_name)[1]
                self.new_file_list[self.new_file_list.index(file)] = None
                self.setTabText(index, tab_name)
                self.setTabToolTip(index, file_name)
                self.signal.emit('file_path>' + file_name)
                return True
            else:
                return False

    # 获取编辑器信号
    def get_editor_signal(self, signal_str):
        self.signal.emit(signal_str)

    # 切换tab事件
    def switch_tab(self, index):
        file_path = self.file_list[index]
        self.signal.emit('file_path>' + file_path)

    # 关闭标签页(需要判断)
    def close_tab(self, index):
        save_file_flag = False
        file_name = self.file_list[index]
        current_text = self.currentWidget().text()
        if os.path.exists(file_name):
            with open(file_name, 'r', encoding='utf-8') as f:
                file_text = f.read()
            if current_text == file_text:
                save_file_flag = False
            else:
                save_file_flag = True
        else:
            save_file_flag = True
        if save_file_flag is True:
            reply = QMessageBox.question(self, '当前文件未保存', '是否保存当前文件', QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Yes)
            if reply == QMessageBox.Yes:
                save_status = self.save_edit_tab()
                if save_status is True:
                    self.removeTab(index)
                    self.file_list.pop(index)
                else:
                    pass
            elif reply == QMessageBox.No:
                self.removeTab(index)
                self.file_list.pop(index)
            elif reply == QMessageBox.Cancel:
                pass
            else:
                pass
        else:
            self.removeTab(index)
            self.file_list.pop(index)
        # 处理tab_name
        if file_name in self.new_file_list:
            tab_index = self.new_file_list.index(file_name)
            self.new_file_list[tab_index] = None
        # 删除完tab后需要修改状态栏
        tab_counts = self.count()
        if tab_counts > 0:
            new_index = self.currentIndex()
            file_path = self.file_list[new_index]
            cursor_position = '[0:0]'
            self.signal.emit('file_path>' + file_path)
            self.signal.emit('cursor_position>' + cursor_position)
        else:
            file_path = 'None'
            cursor_position = '[0:0]'
            self.signal.emit('file_path>' + file_path)
            self.signal.emit('cursor_position>' + cursor_position)


# 窗口app
class MainWindow(QMainWindow):
    def __init__(self, parent=None, title='未命名'):
        super(MainWindow, self).__init__(parent)
        self.setGeometry(100, 100, 1000, 700)
        self.setWindowTitle(title)
        self.setFont(QFont('Consolas', 14, QFont.Bold))
        # 中间widget区域
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        # 工程栏
        self.project_path = MergePath(os.getcwd()).merged_path
        self.project_bar = ProjectBar(self.central_widget, self.project_path)
        # 编辑器设置
        # self.editor = MyQscintilla(self.centralWidget())
        # self.setCentralWidget(self.editor)
        self.editor_widget = EditWidget(self.central_widget)
        self.editor_widget.signal[str].connect(self.get_signal_from_editor)
        # self.setCentralWidget(self.editor_widget)
        # 全局竖直布局
        self.general_v_layout = QVBoxLayout(self.central_widget)
        self.general_v_layout.setContentsMargins(1, 0, 0, 0)
        # 分割窗口布局
        self.splitter_h_general = QSplitter(Qt.Horizontal)
        self.splitter_h_general.setHandleWidth(0)
        self.splitter_h_general.addWidget(self.project_bar)
        self.splitter_h_general.addWidget(self.editor_widget)
        self.splitter_h_general.setStretchFactor(0, 1)
        self.splitter_h_general.setStretchFactor(1, 4)
        self.general_v_layout.addWidget(self.splitter_h_general)
        self.setLayout(self.general_v_layout)

        # 菜单栏
        # 菜单栏
        self.menu_bar = QMenuBar(self)
        self.menu_bar.setObjectName('menu_bar')
        # 设置菜单栏样式
        menu_style = 'QMenu::item {background-color: transparent; padding-left: 5px; padding-right: 5px;}\
                              QMenu::item:selected {background-color: #2DABF9;}'
        self.menu_bar.setStyleSheet(menu_style)
        self.setMenuBar(self.menu_bar)
        # 文件菜单栏
        self.file_bar = self.menu_bar.addMenu('文件')
        self.new_file_action_menu = QAction('新建文件', self)
        self.new_file_action_menu.triggered.connect(self.connect_new_file)
        self.open_file_action_menu = QAction('打开文件', self)
        self.open_file_action_menu.triggered.connect(self.connect_open_file)
        self.save_file_action_menu = QAction('保存文件', self)
        self.save_file_action_menu.triggered.connect(self.connect_save_file)
        self.file_bar.addAction(self.new_file_action_menu)
        self.file_bar.addAction(self.open_file_action_menu)
        self.file_bar.addAction(self.save_file_action_menu)
        # 帮助菜单栏
        self.help_bar = self.menu_bar.addMenu('帮助')
        self.help_action_menu = QAction('操作说明', self)
        # self.help_action_menu.triggered.connect(self.connect_open_file)
        self.help_bar.addAction(self.help_action_menu)
        # 工具栏
        self.tool_bar = self.addToolBar('tool_bar')
        self.new_file_action = QAction(QIcon(Icon.new_file), '新建文件', self)
        self.new_file_action.triggered.connect(self.connect_new_file)
        self.open_file_action = QAction(QIcon(Icon.open_file), '打开文件', self)
        self.open_file_action.triggered.connect(self.connect_open_file)
        self.save_file_action = QAction(QIcon(Icon.save_file), '保存文件', self)
        self.save_file_action.triggered.connect(self.connect_save_file)
        self.tool_bar.addAction(self.new_file_action)
        self.tool_bar.addAction(self.open_file_action)
        self.tool_bar.addAction(self.save_file_action)
        # 状态栏 & 状态栏显示
        self.status_bar = QStatusBar(self)
        self.status_bar.setObjectName('status_bar')
        self.status_bar.setContentsMargins(0, 0, 0, 0)
        self.setStatusBar(self.status_bar)
        # 状态栏内控件
        self.file_icon = QToolButton(self)
        self.file_icon.setStyleSheet('QToolButton{border-image: url(' + Icon.file + ')}')
        self.file_path_label = QLabel(self)
        self.file_path_label.setText('new.xml')
        self.cursor_label = QLabel(self)
        self.cursor_label.setText('0:0')
        # 状态栏布局
        self.status_bar.addPermanentWidget(self.file_icon, stretch=0)
        self.status_bar.addPermanentWidget(self.file_path_label, stretch=5)
        self.status_bar.addPermanentWidget(self.cursor_label, stretch=1)

    # 获取编辑器文本中发出的信号
    def get_signal_from_editor(self, signal_str):
        flag = signal_str.split('>')[0]
        if flag == 'file_path':
            file_path = signal_str.split('>')[1]
            self.file_path_label.setText(file_path)
        elif flag == 'cursor_position':
            cursor_position = signal_str.split('>')[1]
            self.cursor_label.setText(cursor_position)
        else:
            pass

    # 新建文件
    def connect_new_file(self):
        self.editor_widget.new_edit_tab()

    # 打开文件
    def connect_open_file(self):
        self.editor_widget.open_edit_tab()

    # 保存文件
    def connect_save_file(self):
        self.editor_widget.save_edit_tab()


if __name__=='__main__':
    app = QApplication(sys.argv)
    form = MainWindow(None, 'xml-editor')
    form.show()
    app.exec_()