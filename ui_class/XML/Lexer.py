from PyQt5.Qsci import *


# xml解释器
class MyLexerXML(QsciLexerXML):
    def __init__(self, parent):
        super(MyLexerXML, self).__init__(parent)
        # 设置标签大小写敏感
        self.setCaseSensitiveTags(True)
        # 设置自动缩进样式
        self.setAutoIndentStyle(QsciScintilla.AiMaintain)
        # self.setAutoIndentStyle(QsciScintilla.AiOpening)
        # self.setAutoIndentStyle(QsciScintilla.AiClosing)