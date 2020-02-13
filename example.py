import os
import configparser

# cf = configparser.ConfigParser()
# cf.read('config.ini', encoding='utf-8')
#
# print(cf.get('begin_line', 'label'))


file = 'D:\\Code\\arm_fluency\\case\\电台启动.xml'
# file = 'D:/Code/arm_fluency/case/电台启动.xml'
aaa = file.split(os.path.sep)
print(aaa)

print(os.path.sep)