# import sys
# from PyQt5.QtWidgets import *
# from PyQt5.QtGui import QIcon, QBrush, QColor
# from PyQt5.QtCore import Qt
#
#
# class TreeWidgetDemo(QMainWindow):
#     def __init__(self, parent=None):
#         super(TreeWidgetDemo, self).__init__(parent)
#         self.setWindowTitle('TreeWidget 例子')
#
#         self.tree=QTreeWidget()
#         tree_qss = 'QTreeWidget::branch:closed:has-children{image:url(:root_close.png);} \
#                     QTreeWidget::branch:open:has-children{image:url(:root_open.png);}'
#
#         self.tree.setStyleSheet(tree_qss)
#         #设置列数
#         self.tree.setColumnCount(2)
#         #设置树形控件头部的标题
#         self.tree.setHeaderLabels(['Key','Value'])
#
#         #设置根节点
#         root=QTreeWidgetItem(self.tree)
#         root.setText(0,'Root')
#         root.setIcon(0,QIcon('./images/root.png'))
#
#         # todo 优化2 设置根节点的背景颜色
#         brush_red=QBrush(Qt.red)
#         root.setBackground(0,brush_red)
#         brush_blue=QBrush(Qt.blue)
#         root.setBackground(1,brush_blue)
#
#         #设置树形控件的列的宽度
#         self.tree.setColumnWidth(0,150)
#
#         #设置子节点1
#         child1=QTreeWidgetItem()
#         child1.setText(0,'child1')
#         child1.setText(1,'ios')
#         child1.setIcon(0,QIcon('./images/IOS.png'))
#
#         #todo 优化1 设置节点的状态
#         child1.setCheckState(0,Qt.Checked)
#
#         root.addChild(child1)
#
#
#         #设置子节点2
#         child2=QTreeWidgetItem(root)
#         child2.setText(0,'child2')
#         child2.setText(1,'')
#         child2.setIcon(0,QIcon('./images/android.png'))
#
#         #设置子节点3
#         child3=QTreeWidgetItem(child2)
#         child3.setText(0,'child3')
#         child3.setText(1,'android')
#         child3.setIcon(0,QIcon('./images/music.png'))
#
#
#
#         #加载根节点的所有属性与子控件
#         self.tree.addTopLevelItem(root)
#
#         #TODO 优化3 给节点添加响应事件
#         self.tree.clicked.connect(self.onClicked)
#
#
#         #节点全部展开
#         self.tree.expandAll()
#         self.setCentralWidget(self.tree)
#
#     def onClicked(self,qmodeLindex):
#         item=self.tree.currentItem()
#         print('Key=%s,value=%s'%(item.text(0),item.text(1)))
#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     tree = TreeWidgetDemo()
#     tree.show()
#     sys.exit(app.exec_())


# -*- coding: UTF-8 -*-
# 从文件中读取数据
import xml.etree.ElementTree as ET


# 遍历所有的节点
def walkData(root_node, level, result_list):
    temp_list = [level, root_node.tag, root_node.attrib]
    result_list.append(temp_list)
    # 遍历每个子节点
    children_node = root_node.getchildren()
    if len(children_node) == 0:
        return
    for child in children_node:
        walkData(child, level + 1, result_list)
    return


def getXmlData(file_name):
    level = 0  # 节点的深度(层)从0开始
    result_list = []
    root = ET.parse(file_name).getroot()
    walkData(root, level, result_list)
    return result_list


# def update_(result_list):
#     for result in result_list:
#         if result[0] == 1:


if __name__ == '__main__':
    file_name = 'D:/Code/editor/xml/test.xml'
    R = getXmlData(file_name)
    for x in R:
        print(x)
    pass
