import os
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from glv import Icon
from ui_class.Editor import Editor


# 编辑器分页器
class EditorTab(QTabWidget):

    signal = pyqtSignal(str)

    def __init__(self, parent):
        super(EditorTab, self).__init__(parent)
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
        editor = Editor(self)
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
        editor = Editor(self)
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
            editor = Editor(self, file=file)
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