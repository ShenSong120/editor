from PyQt5.QtWidgets import QGraphicsOpacityEffect, QFrame
from PyQt5.QtCore import QPropertyAnimation, Qt
from PyQt5.Qsci import *
from other.glv import View


class MiniMap(QsciScintilla):

    def __init__(self, parent, editor):
        QsciScintilla.__init__(self, parent)
        # 设置最大最小宽度
        self.setMaximumWidth(300)
        self.setMinimumWidth(150)
        self.editor = editor
        # 设置缩放(比原始大小缩小10个档)
        self.zoomIn(-10)
        # 词法分析器(根据父类的lexer类型确认导入哪个词法分析器)
        # lexer_type = type(self.editor.lexer).split('.')[-1]
        lexer_type = str(type(self.editor.lexer))
        if 'QsciLexerXML' in lexer_type:
            self.lexer = QsciLexerXML(self)
        self.setLexer(self.lexer)
        # 缩略图文本
        self.setText(self.editor.text())
        # mini_map可以显示的行数
        self.lines_on_screen = 0
        # 设置鼠标跟踪
        self.setMouseTracking(True)
        # 隐藏拖动条
        # self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.SendScintilla(QsciScintilla.SCI_SETHSCROLLBAR, False)
        self.SendScintilla(QsciScintilla.SCI_SETVSCROLLBAR, False)
        # 设置隐藏选择
        self.SendScintilla(QsciScintilla.SCI_HIDESELECTION, True)
        self.setFolding(QsciScintilla.NoFoldStyle, 1)
        # 设置只读
        self.setReadOnly(True)
        self.setCaretWidth(0)
        # 设置背景透明
        self.setStyleSheet("background: transparent; border: 0px;")
        # 设置透明度
        self.effect = QGraphicsOpacityEffect()
        self.setGraphicsEffect(self.effect)
        self.effect.setOpacity(0.5)
        # 设置滑动面板
        self.slider = Slider(self)
        # 设置鼠标样式(箭头光标)
        self.setCursor(Qt.ArrowCursor)
        # mini_map开关
        if View.mini_map_switch is True:
            self.setHidden(False)
        else:
            self.setHidden(True)

    # 尺寸更改
    def resizeEvent(self, event):
        super(MiniMap, self).resizeEvent(event)
        self.change_slider_width()

    # 鼠标点击事件
    def mousePressEvent(self, event):
        self.click_and_jump_to_current_line(event.pos())

    # 滚轮事件
    def wheelEvent(self, event):
        data = event.angleDelta()
        self.wheel_update(data)

    # 更改slider宽度
    def change_slider_width(self):
        self.lines_on_screen = self.SendScintilla(QsciScintilla.SCI_LINESONSCREEN)
        slider_width = self.width()
        slider_height = int((self.editor.lines_on_screen / self.lines_on_screen) * self.height())
        self.slider.setFixedWidth(slider_width)
        self.slider.setFixedHeight(slider_height)
        self.slider.lines = self.editor.lines_on_screen

    # 缩略图代码更新
    def update_code(self):
        self.setText(self.editor.text())

    # 通过坐标跳转到点击行
    def click_and_jump_to_current_line(self, pos):
        # 确保点击有效
        if self.editor.verticalScrollBar().maximum():
            click_line = int(pos.y() / (self.height() / self.lines_on_screen)) + self.firstVisibleLine()
            value = int((self.editor.verticalScrollBar().maximum()/(self.editor.lines()-self.editor.lines_on_screen)) *
                        (click_line - (self.editor.lines_on_screen / 2)))
            self.editor.verticalScrollBar().setValue(value)

    # 滚轮事件更新
    def wheel_update(self, data):
        # 确保可以滑动
        if self.editor.verticalScrollBar().maximum():
            if data.y() < 0:
                new_value = self.editor.verticalScrollBar().value() + 3
            else:
                new_value = self.editor.verticalScrollBar().value() - 3
            self.editor.verticalScrollBar().setValue(new_value)


class Slider(QFrame):

    def __init__(self, mini_map):
        QFrame.__init__(self, mini_map)
        self.mini_map = mini_map
        self.setStyleSheet("background: gray; border-radius: 3px;")
        # 渲染的行数
        self.lines = 0
        # Opacity
        self.effect = QGraphicsOpacityEffect()
        self.setGraphicsEffect(self.effect)
        self.effect.setOpacity(0.3)
        # Animation
        self.animation = QPropertyAnimation(self.effect)
        self.animation.setDuration(150)
        # Cursor
        self.setCursor(Qt.OpenHandCursor)

    def mouseMoveEvent(self, event):
        super(Slider, self).mouseMoveEvent(event)
        pos = self.mapToParent(event.pos())
        # 触发mini_map进行跳转
        self.mini_map.click_and_jump_to_current_line(pos)

    def mousePressEvent(self, event):
        super(Slider, self).mousePressEvent(event)
        self.setCursor(Qt.ClosedHandCursor)
        pos = self.mapToParent(event.pos())
        # 触发mini_map进行跳转
        self.mini_map.click_and_jump_to_current_line(pos)

    def mouseReleaseEvent(self, event):
        super(Slider, self).mouseReleaseEvent(event)
        self.setCursor(Qt.OpenHandCursor)

    def wheelEvent(self, event):
        data = event.angleDelta()
        self.mini_map.wheel_update(data)
