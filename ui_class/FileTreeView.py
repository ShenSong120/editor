from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class FileTreeView(QTreeView):

    signal = pyqtSignal(str)

    def __init__(self, parent):
        super(FileTreeView, self).__init__(parent)
        self.setItemsExpandable(True)
        self.setExpandsOnDoubleClick(True)
        # 设置允许多选
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)

    # 鼠标点击事件
    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        point = (event.pos().x(), event.pos().y())
        self.signal.emit('click_point>' + str(point))

    # 鼠标双击
    def mouseDoubleClickEvent(self, event):
        super().mouseDoubleClickEvent(event)
        point = (event.pos().x(), event.pos().y())
        self.signal.emit('double_click_point>' + str(point))