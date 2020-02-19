from os import path, mkdir, remove


def init_dir():
    """
    特例, 初始化result文件夹
    """
    dirsrc = './result'
    if path.exists(dirsrc) is False:
        mkdir(dirsrc)


def remove_file(src):
    """
    移除文件
    """
    if path.exists(src):
        remove(src)
