from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from ui_class.XML.Editor import Editor as XML_Editor
from ui_class.XML.MiniMap import MiniMap


class Editor(QWidget):
    signal = pyqtSignal(str)

    def __init__(self, parent, file):
        super(Editor, self).__init__(parent)
        self.editor = XML_Editor(self, file)
        self.mini_map = MiniMap(self.editor)

        self.editor.signal[str].connect(self.get_signal_from_editor)

        self.editor.verticalScrollBar().valueChanged.connect(self.mini_map.update_scroll_bar)
        self.mini_map.verticalScrollBar().valueChanged.connect(self.editor.update_scroll_bar)
        self.editor.textChanged.connect(self.mini_map.update_code)

        self.splitter_h_general = QSplitter(Qt.Horizontal)
        self.splitter_h_general.setHandleWidth(0)
        self.splitter_h_general.addWidget(self.editor)
        self.splitter_h_general.addWidget(self.mini_map)
        self.splitter_h_general.setStretchFactor(0, 6)
        self.splitter_h_general.setStretchFactor(1, 1)

        self.general_layout = QHBoxLayout(self)
        self.general_layout.setContentsMargins(0, 0, 0, 0)
        self.general_layout.addWidget(self.splitter_h_general)

        self.setLayout(self.general_layout)

    # 信号传递
    def get_signal_from_editor(self, signal_str):
        self.signal.emit(signal_str)

    def text(self):
        return self.editor.text()


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    # form = Editor(None, 'D:/Code/editor/xml/test.xml')
    form = Editor(None, 'D:/Code/editor/xml/new.xml')
    form.show()
    app.exec_()
