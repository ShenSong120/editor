# coding:utf-8
from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5.Qsci import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import re
import keyword
import os

'''感谢https://blog.csdn.net/xiaoyangyang20/article/details/68923133?fps=1&locationNum=4
，https://blog.csdn.net/tgbus18990140382/article/details/26136661
，https://qscintilla.com
。'''


class MainWindow(QMainWindow):
    def __init__(self, parent=None, title='未命名'):
        super(MainWindow, self).__init__(parent)
        self.setGeometry(100, 100, 1000, 700)
        self.setWindowTitle(title)
        font = QFont()
        font.setFamily('Courier')
        font.setPointSize(12)
        font.setFixedPitch(True)
        self.setFont(font)
        self.editor = QsciScintilla()
        self.editor.setFont(font)
        self.setCentralWidget(self.editor)
        self.editor.setUtf8(True)
        self.editor.setMarginsFont(font)
        self.editor.setMarginWidth(0, len(str(len(self.editor.text().split('\n')))) * 20)
        self.editor.setMarginLineNumbers(0, True)

        self.editor.setEdgeMode(QsciScintilla.EdgeLine)
        self.editor.setEdgeColumn(80)
        self.editor.setEdgeColor(QColor(0, 0, 0))

        self.editor.setBraceMatching(QsciScintilla.StrictBraceMatch)

        self.editor.setIndentationsUseTabs(True)
        self.editor.setIndentationWidth(4)
        self.editor.setTabIndents(True)
        self.editor.setAutoIndent(True)
        self.editor.setBackspaceUnindents(True)
        self.editor.setTabWidth(4)

        self.editor.setCaretLineVisible(True)
        self.editor.setCaretLineBackgroundColor(QColor('#FFFFCD'))

        self.editor.setIndentationGuides(True)

        self.editor.setFolding(QsciScintilla.PlainFoldStyle)
        self.editor.setMarginWidth(2, 12)

        self.editor.markerDefine(QsciScintilla.Minus, QsciScintilla.SC_MARKNUM_FOLDEROPEN)
        self.editor.markerDefine(QsciScintilla.Plus, QsciScintilla.SC_MARKNUM_FOLDER)
        self.editor.markerDefine(QsciScintilla.Minus, QsciScintilla.SC_MARKNUM_FOLDEROPENMID)
        self.editor.markerDefine(QsciScintilla.Plus, QsciScintilla.SC_MARKNUM_FOLDEREND)

        self.editor.setMarkerBackgroundColor(QColor("#FFFFFF"), QsciScintilla.SC_MARKNUM_FOLDEREND)
        self.editor.setMarkerForegroundColor(QColor("#272727"), QsciScintilla.SC_MARKNUM_FOLDEREND)
        self.editor.setMarkerBackgroundColor(QColor("#FFFFFF"), QsciScintilla.SC_MARKNUM_FOLDEROPENMID)
        self.editor.setMarkerForegroundColor(QColor("#272727"), QsciScintilla.SC_MARKNUM_FOLDEROPENMID)
        self.editor.setAutoCompletionSource(QsciScintilla.AcsAll)
        self.editor.setAutoCompletionCaseSensitivity(True)
        self.editor.setAutoCompletionReplaceWord(False)
        self.editor.setAutoCompletionThreshold(1)
        self.editor.setAutoCompletionUseSingle(QsciScintilla.AcusExplicit)

        # self.lexer = highlight(self.editor)
        self.lexer = QsciLexerPython(self.editor)
        self.lexer.setDefaultFont(QFont('Consolas', 12))
        self.editor.setLexer(self.lexer)
        self.mod = False
        self.__api = QsciAPIs(self.lexer)
        autocompletions = keyword.kwlist + ["abs", "all", "any", "basestring", "bool",
                                            "callable", "chr", "classmethod", "cmp", "compile",
                                            "complex", "delattr", "dict", "dir", "divmod",
                                            "enumerate", "eval", "execfile", "exit", "file",
                                            "filter", "float", "frozenset", "getattr", "globals",
                                            "hasattr", "hex", "id", "int", "isinstance",
                                            "issubclass", "iter", "len", "list", "locals", "map",
                                            "max", "min", "object", "oct", "open", "ord", "pow",
                                            "property", "range", "reduce", "repr", "reversed",
                                            "round", "set", "setattr", "slice", "sorted",
                                            "staticmethod", "str", "sum", "super", "tuple", "type",
                                            "vars", "zip", 'print']
        for ac in autocompletions:
            self.__api.add(ac)
        self.__api.prepare()
        self.editor.autoCompleteFromAll()

        # 设置函数名为关键字2    KeyWord = sdcc_kwlistcc  ;KeywordSet2 = 函数名
        # self.editor.SendScintilla(QsciScintilla.SCI_SETKEYWORDS, 0, " ".join(autocompletions).encode(encoding='utf-8'))
        self.editor.SendScintilla(QsciScintilla.SCI_STYLESETFORE, QsciLexerCPP.KeywordSet2, 0x7f0000)
        # self.editor.SendScintilla(QsciScintilla.SCI_SETKEYWORDS, 1, " ".join(g_allFuncList).encode(encoding='utf-8'))

        self.editor.textChanged.connect(self.changed)
        self.editor.userListActivated.connect(self.get_selected_item)


    def changed(self):
        self.mod = True
        self.editor.setMarginWidth(0, len(str(len(self.editor.text().split('\n')))) * 20)

    def get_selected_item(self, id, item):
        print(id, item)



def main():
    import sys
    app = QApplication(sys.argv)
    form = MainWindow(None, 'python-editor')
    form.show()
    app.exec_()


main()