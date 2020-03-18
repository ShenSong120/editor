class Param:
    config_file = 'config/config.ini'
    translator_file = 'config/qt_zh_CN.qm'
    # 打开的文件工程目录
    project_path = None


class Icon:
    close_tab = 'config/icon/close_tab.png'
    close_tab_hover = 'config/icon/close_tab_hover.png'
    function = 'config/icon/function.png'
    word = 'config/icon/word.png'
    new_file = 'config/icon/new_file.png'
    open_folder = 'config/icon/open_folder.png'
    new = 'config/icon/new.png'
    open_file = 'config/icon/open_file.png'
    save_file = 'config/icon/save_file.png'
    save_as_file = 'config/icon/save_as_file.png'
    file = 'config/icon/file.png'
    path = 'config/icon/path.png'
    last = 'config/icon/last.png'
    next = 'config/icon/next.png'
    close = 'config/icon/close.png'
    enter = 'config/icon/enter.png'
    clear_text = 'config/icon/clear_text.png'
    checked = 'config/icon/checked.png'
    unchecked = 'config/icon/unchecked.png'
    undo = 'config/icon/undo.png'
    redo = 'config/icon/redo.png'
    cut = 'config/icon/cut.png'
    copy = 'config/icon/copy.png'
    paste = 'config/icon/paste.png'
    delete = 'config/icon/delete.png'
    select_all = 'config/icon/select_all.png'
    comment = 'config/icon/comment.png'
    search = 'config/icon/search.png'
    replace = 'config/icon/replace.png'
    root_open = 'config/icon/root_open.png'
    root_close = 'config/icon/root_close.png'
    xml_tag = 'config/icon/xml_tag.png'
    cursor = 'config/icon/cursor.png'
    mini_map = 'config/icon/mini_map.png'
    structure = 'config/icon/structure.png'


# 样式
class BeautifyStyle:
    font_family = 'font-family: Times New Roman;'
    font_size = 'font-size: 13pt;'
    file_dialog_qss = 'QFileDialog {font-family: Times New Roman; background-color: beige;}'
    label_qss = "QLabel{border: 1px solid #7A7A7A;}"


# 编辑器动作
class EditorAction:
    undo = 'undo'
    redo = 'redo'
    cut = 'cut'
    copy = 'copy'
    paste = 'paste'
    delete = 'delete'
    select_all = 'select_all'
    comment = 'comment'
    search = 'search'
    replace = 'replace'


# 视图中的控件开关
class View:
    # mini_map开关
    mini_map_switch = False


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
