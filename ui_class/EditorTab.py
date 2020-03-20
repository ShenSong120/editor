import os
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from other.glv import Icon
# from ui_class.XML.Editor import Editor
from ui_class.XML.EditorWithMiniMap import Editor


# 编辑器分页器
class EditorTab(QTabWidget):

    signal = pyqtSignal(str)

    def __init__(self, parent):
        super(EditorTab, self).__init__(parent)
        self.parent = parent
        # 打开的文件列表(保存文件列表)
        self.file_list = []
        # 设置tab可以关闭
        self.setTabsClosable(True)
        # 样式设置font-family:Arial;字体对tab显示有影响
        style_sheet = 'QTabWidget:pane{border: 1px solid #7A7A7A; top: -1px;}\
                       QTabWidget:tab-bar{border: 1px solid blue; top: 0px; alignment:left; background: blue}\
                       QTabBar::tab{height: 25px; margin-right: 0px; margin-bottom:-3px; padding-left: 5px; padding-right: 5px;}\
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

    # 新建文件
    def new_edit_tab(self, file):
        if file in self.file_list:
            index = self.file_list.index(file)
            self.setCurrentIndex(index)
        else:
            self.file_list.append(file)
            tab_name = os.path.split(file)[1]
            editor = Editor(self, file=file)
            editor.signal[str].connect(self.get_editor_signal)
            self.addTab(editor, tab_name)
            self.setCurrentWidget(editor)
            index = self.indexOf(editor)
            self.setTabToolTip(index, tab_name)

    # 打开文件
    def open_edit_tab(self, file=None):
        if file is None:
            file, file_type = QFileDialog.getOpenFileName(self, "选取文件", "./", "Xml Files (*.xml)", options=QFileDialog.DontUseNativeDialog)
        if file:
            if file in self.file_list:
                index = self.file_list.index(file)
                self.setCurrentIndex(index)
            else:
                self.file_list.append(file)
                tab_name = os.path.split(file)[1]
                editor = Editor(self, file=file)
                editor.signal[str].connect(self.get_editor_signal)
                self.addTab(editor, tab_name)
                self.setCurrentWidget(editor)
                index = self.indexOf(editor)
                self.setTabToolTip(index, file)

    # 保存文件
    def save_edit_tab(self, file=None):
        if file is None:
            index = self.currentIndex()
            editor = self.currentWidget()
            file = str(self.file_list[index])
        else:
            index = self.file_list.index(file)
            editor = self.widget(index)
            file = file
        if os.path.exists(file):
            with open(file, 'w+', encoding='utf-8') as f:
                text = editor.text()
                f.write(text)
            return True

    # 文件另存
    def save_file_as_tab(self):
        index = self.currentIndex()
        editor = self.currentWidget()
        file = str(self.file_list[index])
        current_root_path = os.path.dirname(file)
        file_name, file_type = QFileDialog.getSaveFileName(self, '文件另存', current_root_path, 'Xml Files (*.xml);;All Files (*)', options=QFileDialog.DontUseNativeDialog)
        if file_name:
            with open(file_name, 'w', encoding='utf-8') as f:
                text = editor.text()
                f.write(text)

    # 获取编辑器信号
    def get_editor_signal(self, signal_str):
        flag = signal_str.split('>')[0]
        # 光标信号
        if flag == 'cursor_position':
            self.signal.emit(signal_str)
        # 函数跳转
        elif flag == 'dump_in_function':
            self.signal.emit(signal_str)
        # 保存文件
        elif flag == 'save_file':
            self.save_edit_tab()
            # 更新tree
            file_path = self.file_list[self.currentIndex()]
            self.signal.emit('update_tree>' + file_path)
        else:
            self.signal.emit(signal_str)

    # 切换tab事件
    def switch_tab(self, index):
        # 更新工具栏动作状态
        editor = self.currentWidget()
        if editor is not None:
            editor.judge_action_enable()
            file_path = self.file_list[index]
            self.signal.emit('file_path>' + file_path)
            # 更新树
            self.signal.emit('update_tree>' + file_path)
        else:
            self.signal.emit('close_all_tab>')

    # 关闭标签页(需要判断)
    def close_tab(self, index):
        # 关闭标签页信号
        file_path = self.file_list[index]
        self.signal.emit('remove_tree>' + file_path)
        # 溢出标签
        self.removeTab(index)
        self.file_list.pop(index)
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
