from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from ui_class.XML.Editor import Editor as XML_Editor
from ui_class.XML.MiniMap import MiniMap


class Editor(QWidget):
    signal = pyqtSignal(str)

    def __init__(self, parent, file):
        super(Editor, self).__init__(parent)
        self.editor = XML_Editor(self, file)
        self.mini_map = MiniMap(self, self.editor)

        self.editor.signal[str].connect(self.get_signal_from_editor)

        self.editor.verticalScrollBar().valueChanged.connect(self.editor_vertical_scroll_bar_value_changed)
        self.mini_map.verticalScrollBar().valueChanged.connect(self.mini_map_vertical_scroll_bar_value_changed)

        self.editor.textChanged.connect(self.mini_map.update_code)
        self.editor.linesChanged.connect(self.editor_lines_changed)

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
        # 编辑器和mini_map宽度改变(需要重新调整所有mini_map)
        if signal_str.split('>')[0] == 'editor_width_changed':
            self.mini_map.change_slider_width()
        # 光标移动事件
        elif signal_str.split('>')[0] == 'cursor_position':
            self.editor_vertical_scroll_bar_value_changed(self.editor.verticalScrollBar().value())
            self.signal.emit(signal_str)
        else:
            self.signal.emit(signal_str)

    # 返回编辑器文本
    def text(self):
        return self.editor.text()

    # 更新动作使能(并发送信号给窗口动作)
    def judge_action_enable(self):
        self.editor.judge_action_enable()

    # editor行数更改事件
    def editor_lines_changed(self):
        self.editor_vertical_scroll_bar_value_changed(self.editor.verticalScrollBar().value())

    # editor滚动条滚动事件
    def editor_vertical_scroll_bar_value_changed(self, value):
        # editor滚动的时候, 禁止mini_map滚动触发(防止混乱触发)
        self.mini_map.verticalScrollBar().valueChanged.disconnect(self.mini_map_vertical_scroll_bar_value_changed)
        # 确保editor可以滚动
        max_value = self.editor.verticalScrollBar().maximum() if self.editor.verticalScrollBar().maximum() else 1
        scale = value / max_value
        mini_map_value = int(scale * self.mini_map.verticalScrollBar().maximum())
        self.mini_map.verticalScrollBar().setValue(mini_map_value)
        # 更新mini_map中的slider
        self.update_mini_map_slider()
        # 同步完mini_map后, 打开mini_map滚动触发
        self.mini_map.verticalScrollBar().valueChanged.connect(self.mini_map_vertical_scroll_bar_value_changed)

    # mini_map滚动条滚动事件
    def mini_map_vertical_scroll_bar_value_changed(self, value):
        # mini_map滚动的时候, 禁止editor滚动触发(防止混乱触发)
        self.editor.verticalScrollBar().valueChanged.disconnect(self.editor_vertical_scroll_bar_value_changed)
        # 确保editor可以滚动
        max_value = self.editor.verticalScrollBar().maximum() if self.editor.verticalScrollBar().maximum() else 1
        scale = value / max_value
        editor_value = int(scale * self.editor.verticalScrollBar().maximum())
        self.editor.verticalScrollBar().setValue(editor_value)
        # 更新mini_map中的slider
        self.update_mini_map_slider()
        # 同步完editor后, 打开editor滚动触发
        self.editor.verticalScrollBar().valueChanged.connect(self.editor_vertical_scroll_bar_value_changed)

    # mini_map的slider滚动更新
    def update_mini_map_slider(self):
        # 确保滚动不会出现问题
        if self.editor.verticalScrollBar().maximum():
            # 获取屏幕展示的起始行号
            editor_first_line = self.editor.firstVisibleLine()
            mini_map_first_line = self.mini_map.firstVisibleLine()
            slider_height = int((editor_first_line - mini_map_first_line) *
                                (self.mini_map.height() / self.mini_map.lines_on_screen))
            self.mini_map.slider.move(0, slider_height)
        else:
            self.mini_map.slider.move(0, 0)


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    form = Editor(None, 'D:/Code/editor/xml/new.xml')
    form.show()
    app.exec_()
