import os
import configparser

# cf = configparser.ConfigParser()
# cf.read('config.ini', encoding='utf-8')
#
# print(cf.get('begin_line', 'label'))


file = 'D:/Code/arm_fluency/case/电台启动.xml'
tab_name = os.path.split(file)[1]
print(tab_name)