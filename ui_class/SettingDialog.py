from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from other.CaseConfigParser import CaseConfigParser
from other.glv import Param


class Setting(QDialog):
    signal = pyqtSignal(str)

    def __init__(self, parent):
        super(Setting, self).__init__(parent=parent)
        self.setWindowTitle('设置')
        self.resize(800, 500)
        # 获取配置文件对象
        self.config = CaseConfigParser()
        self.config.read(Param.config_file, encoding='utf-8')
        # 获取需要传递的值
        self.tag_list = self.config.options('tags')
        self.attribute_name_list = self.config.options('attributes')
        self.attribute_value_list = self.config.options('attribute_values')
        self.function_name_list = self.config.options('function')
        self.function_value_list = []
        for function_name in self.function_name_list:
            function_value = self.config.get('function', function_name)
            function_value = function_value.replace('\\n', '\n')
            function_value = function_value.replace('\\t', '\t')
            self.function_value_list.append(function_value)
        # 设置三个tab页
        self.tag_tab = OtherWindow('tags', self.tag_list)
        self.tag_tab.signal[str].connect(self.get_signal)
        self.attrib_name_tab = OtherWindow('attributes', self.attribute_name_list)
        self.attrib_name_tab.signal[str].connect(self.get_signal)
        self.attrib_value_tab = OtherWindow('attribute_values', self.attribute_value_list)
        self.attrib_value_tab.signal[str].connect(self.get_signal)
        self.function_tab = FunctionWindow('function', self.function_name_list, self.function_value_list)
        self.function_tab.signal[str].connect(self.get_signal)
        # tab_widget窗口
        self.tab_widget = QTabWidget(self)
        tab_widget_qss = 'QTabWidget:pane{border: 1px solid #7A7A7A; top: -1px;}\
                          QTabWidget:tab-bar{border: 1px solid blue; top: 0px; alignment:left; background: blue}\
                          QTabBar::tab{height: 25px; margin-right: 0px; margin-bottom:-3px; padding-left: 5px; padding-right: 5px;}\
                          QTabBar::tab:selected{border: 1px solid #0099FF; color: #0099FF; background-color: white; border-top: 1px solid #0099FF; border-bottom: 5px solid #0099FF;}\
                          QTabBar::tab:!selected{border: 1px solid #7A7A7A;}\
                          QTabBar::tab:!selected:hover{border: 1px solid #7A7A7A; color: #0099CC;}'
        self.tab_widget.setStyleSheet(tab_widget_qss)
        self.tab_widget.addTab(self.tag_tab, '标签')
        self.tab_widget.addTab(self.attrib_name_tab, '属性名')
        self.tab_widget.addTab(self.attrib_value_tab, '属性值')
        self.tab_widget.addTab(self.function_tab, '代码块')
        # 总体布局
        self.general_layout = QHBoxLayout()
        self.general_layout.setSpacing(0)
        self.general_layout.setContentsMargins(0, 0, 0, 0)
        self.general_layout.addWidget(self.tab_widget)
        self.setLayout(self.general_layout)

    # 获取子窗口信号
    def get_signal(self, signal_str):
        self.signal.emit(signal_str)


# 设置其他tab子窗口(tag, attrib, attrib_value等)
class OtherWindow(QWidget):
    signal = pyqtSignal(str)

    def __init__(self, section_type, option_list, parent=None):
        super(OtherWindow, self).__init__(parent=parent)
        # 传入的section_type, option和value
        self.section_type = section_type
        self.option_list = option_list
        # 装入自定义文件
        self.list_widget = QListWidget(self)
        self.list_widget.addItems(self.option_list)
        self.list_widget.setCurrentRow(0)
        self.list_widget.currentRowChanged.connect(self.item_row_changed)
        # 堆叠窗口
        self.text_edit = QTextEdit(self)
        self.text_edit.setStyleSheet('font-family:Consolas;')
        metrics = QFontMetrics(self.text_edit.font())
        self.text_edit.setTabStopWidth(4 * metrics.width(' '))
        self.text_edit.ensureCursorVisible()
        self.text_edit.setLineWrapMode(QTextEdit.FixedPixelWidth)
        self.text_edit.setWordWrapMode(QTextOption.NoWrap)
        self.text_edit.setReadOnly(True)
        self.item_row_changed(0)
        # 底部按钮
        self.add_button = QPushButton('添加')
        self.delete_button = QPushButton('删除')
        # 按钮触发事件
        self.add_button.clicked.connect(self.add_option_and_value)
        self.delete_button.clicked.connect(self.delete_option_and_value)
        # 按钮布局
        self.button_layout = QHBoxLayout()
        self.button_layout.addStretch(1)
        self.button_layout.addWidget(self.add_button)
        self.button_layout.addStretch(1)
        self.button_layout.addWidget(self.delete_button)
        self.button_layout.addStretch(1)
        # 布局
        self.h_layout = QHBoxLayout()
        self.h_layout.setSpacing(0)
        self.h_layout.setContentsMargins(0, 0, 0, 0)
        self.h_layout.addWidget(self.list_widget)
        self.h_layout.addWidget(self.text_edit)
        self.h_layout.setStretch(0, 1)
        self.h_layout.setStretch(1, 1)
        # 整体布局
        self.general_layout = QVBoxLayout()
        self.general_layout.setSpacing(0)
        self.general_layout.setContentsMargins(0, 0, 0, 0)
        self.general_layout.addLayout(self.h_layout)
        self.general_layout.addLayout(self.button_layout)
        self.setLayout(self.general_layout)

    # 配置文件更新项
    def config_update_option(self, option, value):
        # 实例化configParser对象
        config = CaseConfigParser()
        # -read读取ini文件
        config.read(Param.config_file, encoding='utf-8')
        config.set(self.section_type, option, value)  # 给type分组设置值
        with open(Param.config_file, 'w', encoding='utf-8') as f:
            config.write(f)
        self.signal.emit('config_update_option')

    # 配置文件删除项
    def config_remove_option(self, option):
        # 实例化configParser对象
        config = CaseConfigParser()
        # -read读取ini文件
        config.read(Param.config_file, encoding='utf-8')
        config.remove_option(self.section_type, option)  # 给type分组设置值
        with open(Param.config_file, 'w', encoding='utf-8') as f:
            config.write(f)
        self.signal.emit('config_update_option')

    # 增加选项
    def add_option_and_value(self):
        option, ok = QInputDialog.getText(self, "item名字", "请输入选项名字:", QLineEdit.Normal, "new_item")
        if ok:
            if option not in self.option_list:
                self.list_widget.addItem(option)
                self.option_list.append(option)
                # 将选项更新入配置文件
                value = option + '=""' if self.section_type == 'attributes' else option
                self.config_update_option(option, value)
                row = self.option_list.index(option)
                self.list_widget.setCurrentRow(row)
            else:
                QMessageBox.information(self, "提示", "新建的选项已经存在\n请重新输入选项名字", QMessageBox.Ok)
                self.add_option_and_value()

    # remove option
    def delete_option_and_value(self):
        row = self.list_widget.currentRow()
        item = self.list_widget.takeItem(row)
        self.list_widget.removeItemWidget(item)
        # 配置文件中删除
        self.config_remove_option(self.option_list[row])
        # 去掉删除项
        self.option_list.pop(row)

    # 切换
    def item_row_changed(self, row):
        option = self.option_list[row]
        if self.section_type == 'attributes':
            value = option + '=""'
        else:
            value = option
        self.text_edit.setText(value)


# 设置自定义函数tab子窗口
class FunctionWindow(QWidget):
    signal = pyqtSignal(str)

    def __init__(self, section_type, function_name_list, function_value_list, parent=None):
        super(FunctionWindow, self).__init__(parent=parent)
        # 传入的function的name和value
        self.section_type = section_type
        self.function_name_list = function_name_list
        self.function_value_list = function_value_list
        # 装入自定义文件
        self.list_widget = QListWidget(self)
        self.list_widget.addItems(self.function_name_list)
        self.list_widget.setCurrentRow(0)
        self.list_widget.currentRowChanged.connect(self.item_row_changed)
        # 堆叠窗口
        self.text_edit = QTextEdit(self)
        self.text_edit.setStyleSheet('font-family:Consolas; background: #FFFFFF')
        metrics = QFontMetrics(self.text_edit.font())
        self.text_edit.setTabStopWidth(4 * metrics.width(' '))
        self.text_edit.ensureCursorVisible()
        self.text_edit.setLineWrapMode(QTextEdit.FixedPixelWidth)
        self.text_edit.setWordWrapMode(QTextOption.NoWrap)
        self.text_edit.setReadOnly(True)
        self.item_row_changed(0)
        # 底部按钮
        self.add_button = QPushButton('添加')
        self.modify_button = QPushButton('修改')
        self.delete_button = QPushButton('删除')
        self.save_button = QPushButton('保存')
        # 按钮触发事件
        self.add_button.clicked.connect(self.add_option_and_value)
        self.modify_button.clicked.connect(self.modify_option_and_value)
        self.delete_button.clicked.connect(self.delete_option_and_value)
        self.save_button.clicked.connect(self.save_option_and_value)
        # 按钮布局
        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.add_button)
        self.button_layout.addStretch(1)
        self.button_layout.addWidget(self.modify_button)
        self.button_layout.addStretch(1)
        self.button_layout.addWidget(self.save_button)
        self.button_layout.addStretch(1)
        self.button_layout.addWidget(self.delete_button)
        # 布局
        self.h_layout = QHBoxLayout()
        self.h_layout.setSpacing(0)
        self.h_layout.setContentsMargins(0, 0, 0, 0)
        self.h_layout.addWidget(self.list_widget)
        self.h_layout.addWidget(self.text_edit)
        self.h_layout.setStretch(0, 1)
        self.h_layout.setStretch(1, 1)
        # 整体布局
        self.general_layout = QVBoxLayout()
        self.general_layout.setSpacing(0)
        self.general_layout.setContentsMargins(0, 0, 0, 0)
        self.general_layout.addLayout(self.h_layout)
        self.general_layout.addLayout(self.button_layout)
        self.setLayout(self.general_layout)

    # 配置文件更新项
    def config_update_option(self, option, value):
        # 实例化configParser对象
        config = CaseConfigParser()
        # -read读取ini文件
        config.read(Param.config_file, encoding='utf-8')
        config.set(self.section_type, option, value)  # 给type分组设置值
        with open(Param.config_file, 'w', encoding='utf-8') as f:
            config.write(f)
        self.signal.emit('config_update_option')

    # 配置文件删除项
    def config_remove_option(self, option):
        # 实例化configParser对象
        config = CaseConfigParser()
        # -read读取ini文件
        config.read(Param.config_file, encoding='utf-8')
        config.remove_option(self.section_type, option)  # 给type分组设置值
        with open(Param.config_file, 'w', encoding='utf-8') as f:
            config.write(f)
        self.signal.emit('config_update_option')

    # 配置文件增加选项
    def add_option_and_value(self):
        function_name, ok = QInputDialog.getText(self, "item名字", "请输入选项名字:", QLineEdit.Normal, "new_item")
        if ok:
            if function_name not in self.function_name_list:
                self.function_name_list.append(function_name)
                self.list_widget.addItem(function_name)
                self.list_widget.currentRowChanged.disconnect(self.item_row_changed)
                self.list_widget.setCurrentRow(self.function_name_list.index(function_name))
                self.text_edit.clear()
                self.text_edit.setReadOnly(False)
                self.text_edit.setStyleSheet('font-family:Consolas; background: #CCFFCC')
                self.text_edit.setPlaceholderText('请输入代码块内容后点击保存按钮......')
                self.add_button.setEnabled(False)
                self.modify_button.setEnabled(False)
                self.delete_button.setEnabled(False)
                self.list_widget.setEnabled(False)
            else:
                QMessageBox.information(self, "提示", "新建的选项已经存在\n请重新输入选项名字", QMessageBox.Ok)
                self.add_option_and_value()

    # 修改代码块
    def modify_option_and_value(self):
        index = self.list_widget.currentRow()
        self.function_value_list.pop(index)
        self.text_edit.setReadOnly(False)
        self.text_edit.setStyleSheet('font-family:Consolas; background: #CCFFCC')
        self.add_button.setEnabled(False)
        self.modify_button.setEnabled(False)
        self.delete_button.setEnabled(False)
        self.list_widget.setEnabled(False)

    # 删除代码块
    def delete_option_and_value(self):
        row = self.list_widget.currentRow()
        item = self.list_widget.takeItem(row)
        self.list_widget.removeItemWidget(item)
        # 配置文件中删除
        self.config_remove_option(self.function_name_list[row])
        # 去掉删除项
        self.function_name_list.pop(row)
        self.function_value_list.pop(row)

    # 保存更改
    def save_option_and_value(self):
        function_value = self.text_edit.toPlainText()
        index = self.list_widget.currentRow()
        self.function_value_list.insert(index, function_value)
        self.text_edit.setReadOnly(True)
        self.add_button.setEnabled(True)
        self.modify_button.setEnabled(True)
        self.delete_button.setEnabled(True)
        self.list_widget.setEnabled(True)
        self.list_widget.currentRowChanged.connect(self.item_row_changed)
        self.text_edit.setStyleSheet('font-family:Consolas; background: #FFFFFF')
        # 更新配置文件
        option = self.function_name_list[index]
        value = self.function_value_list[index]
        value = value.replace('\t', '\\t')
        value = value.replace('\n', '\\n')
        self.config_update_option(option, value)

    # 切换
    def item_row_changed(self, row):
        function_name = self.function_name_list[row]
        function_value = self.function_value_list[self.function_name_list.index(function_name)]
        self.text_edit.setText(function_value)
