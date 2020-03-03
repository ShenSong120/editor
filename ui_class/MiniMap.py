from PyQt5.QtWidgets import QGraphicsOpacityEffect, QFrame
from PyQt5.QtCore import QPropertyAnimation, Qt
from PyQt5.Qsci import QsciScintilla


class MiniMap(QsciScintilla):

    def __init__(self, editor):
        QsciScintilla.__init__(self, editor)
        self.editor = editor
        self.indentation = self.editor.indentation
        self.setLexer(self.editor.lexer())
        # Configuración Scintilla
        self.setMouseTracking(True)
        self.SendScintilla(QsciScintilla.SCI_SETHSCROLLBAR, False)
        self.SendScintilla(QsciScintilla.SCI_HIDESELECTION, True)
        self.setFolding(QsciScintilla.NoFoldStyle, 1)
        self.setReadOnly(True)
        self.setCaretWidth(0)
        self.setStyleSheet("background: transparent; border: 0px;")
        # Opacity
        self.effect = QGraphicsOpacityEffect()
        self.setGraphicsEffect(self.effect)
        self.effect.setOpacity(0.5)
        # Deslizador
        self.slider = Slider(self)
        self.slider.hide()

    def resizeEvent(self, event):
        super(MiniMap, self).resizeEvent(event)
        self.slider.setFixedWidth(self.width())
        lines_on_screen = self.editor.SendScintilla(QsciScintilla.SCI_LINESONSCREEN)
        self.slider.setFixedHeight(lines_on_screen * 4)

    def update_geometry(self):
        self.setFixedHeight(self.editor.height())
        self.setFixedWidth(self.editor.width() * 0.13)
        x = self.editor.width() - self.width()
        self.move(x, 0)
        self.zoomIn(-3)

    def update_code(self):
        text = self.editor.text().replace('\t', ' ' * self.indentation)
        self.setText(text)

    def leaveEvent(self, event):
        super(MiniMap, self).leaveEvent(event)
        self.slider.animation.setStartValue(0.2)
        self.slider.animation.setEndValue(0)
        self.slider.animation.start()

    def enterEvent(self, event):
        super(MiniMap, self).enterEvent(event)
        if not self.slider.isVisible():
            self.slider.show()
        else:
            self.slider.animation.setStartValue(0)
            self.slider.animation.setEndValue(0.2)
            self.slider.animation.start()


class Slider(QFrame):

    def __init__(self, mini_map):
        QFrame.__init__(self, mini_map)
        self.mini_map = mini_map
        self.setStyleSheet("background: gray; border-radius: 3px;")
        # Opacity
        self.effect = QGraphicsOpacityEffect()
        self.setGraphicsEffect(self.effect)
        self.effect.setOpacity(0.2)
        # Animación
        self.animation = QPropertyAnimation(self.effect, "opacity")
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
        self.mini_map.weditor.verticalScrollBar().setValue(pos.y())
        self.mini_map.verticalScrollBar().setSliderPosition(
            self.mini_map.verticalScrollBar().sliderPosition() + 2)
        self.mini_map.verticalScrollBar().setValue(pos.y() - event.pos().y())

    def mousePressEvent(self, event):
        super(Slider, self).mousePressEvent(event)
        self.setCursor(Qt.ClosedHandCursor)

    def mouseReleaseEvent(self, event):
        super(Slider, self).mouseReleaseEvent(event)
        self.setCursor(Qt.OpenHandCursor)
