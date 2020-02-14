class Icon:
    close_tab = 'icon/close_tab.png'
    close_tab_hover = 'icon/close_tab_hover.png'
    function = 'icon/function.png'
    word = 'icon/word.png'
    new_file = 'icon/new_file.png'
    open_file = 'icon/open_file.png'
    save_file = 'icon/save_file.png'
    save_as_file = 'icon/save_as_file.png'
    file = 'icon/file.png'


# 样式
class BeautifyStyle:
    # font_family = 'font-family: Times New Roman;'
    font_family = 'font-family: Consolas;'
    font_size = 'font-size: 13pt;'
    file_dialog_qss = 'QFileDialog {font-family: Times New Roman; background-color: beige;}'


# 文件格式统一
class MergePath:
    merged_path = None

    def __init__(self, *args):
        file_sep_list = []
        for arg in args:
            if '\\' in arg:
                file_sep_list += arg.split('\\')
            else:
                file_sep_list += arg.split('/')
        self.merged_path = '/'.join(file_sep_list)
