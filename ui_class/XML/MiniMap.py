from PyQt5.QtWidgets import QGraphicsOpacityEffect, QFrame
from PyQt5.QtCore import QPropertyAnimation, Qt
from PyQt5.Qsci import QsciScintilla


class MiniMap(QsciScintilla):

    def __init__(self, parent, editor):
        QsciScintilla.__init__(self, parent)
        # 设置最大最小宽度
        self.setMaximumWidth(300)
        self.setMinimumWidth(150)
        self.editor = editor
        # 设置缩放(比原始大小缩小10个档)
        self.zoomIn(-10)
        # 词法分析器
        self.setLexer(self.editor.lexer)
        # 缩略图文本
        self.setText(self.editor.text())
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

    # 尺寸更改
    def resizeEvent(self, event):
        super(MiniMap, self).resizeEvent(event)
        self.change_slider_width()

    # 更改slider宽度
    def change_slider_width(self):
        self.slider.setFixedWidth(self.width())
        self.slider.setFixedHeight(self.editor.lines_on_screen * 4)

    # 更新滚动值
    def update_scroll_bar(self, value):
        self.verticalScrollBar().setValue(value)

    # def update_geometry(self):
    #     self.setFixedHeight(self.editor.height())
    #     self.setFixedWidth(self.editor.width() * 0.13)
    #     x = self.editor.width() - self.width()
    #     self.move(x, 0)
    #     self.zoomIn(-3)

    # 缩略图代码更新
    def update_code(self):
        self.setText(self.editor.text())

    # def leaveEvent(self, event):
    #     super(MiniMap, self).leaveEvent(event)
    #     self.slider.animation.setStartValue(0.2)
    #     self.slider.animation.setEndValue(0)
    #     self.slider.animation.start()
    #
    # def enterEvent(self, event):
    #     super(MiniMap, self).enterEvent(event)
    #     if not self.slider.isVisible():
    #         self.slider.show()
    #     else:
    #         self.slider.animation.setStartValue(0)
    #         self.slider.animation.setEndValue(0.2)
    #         self.slider.animation.start()


class Slider(QFrame):

    def __init__(self, mini_map):
        QFrame.__init__(self, mini_map)
        self.mini_map = mini_map
        self.setStyleSheet("background: gray; border-radius: 3px;")
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
        dy = pos.y() - (self.height() / 2)
        if dy < 0:
            dy = 0
        self.move(0, dy)
        pos.setY(pos.y() - event.pos().y())
        self.mini_map.editor.verticalScrollBar().setValue(pos.y())
        self.mini_map.verticalScrollBar().setSliderPosition(self.mini_map.verticalScrollBar().sliderPosition() + 2)
        self.mini_map.verticalScrollBar().setValue(pos.y() - event.pos().y())

    def mousePressEvent(self, event):
        super(Slider, self).mousePressEvent(event)
        self.setCursor(Qt.ClosedHandCursor)

    def mouseReleaseEvent(self, event):
        super(Slider, self).mouseReleaseEvent(event)
        self.setCursor(Qt.OpenHandCursor)
