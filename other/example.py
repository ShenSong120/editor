import os
import re

xml_text = '<case name="ss"><action></action></case>'

aaa = re.findall('<.[^<>]*>', xml_text)

print(aaa)