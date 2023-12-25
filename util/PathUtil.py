import os


def get_name_without_suffix(file_list):
    """
    获取文件名称，不包含后缀名
    :param file_list: 文件列表
    :return:
    """
    name_list = []
    for file in file_list:
        name_list.append(file.split('.')[0])

    return name_list


def mkdir_by_list(path, name_list):
    """
    根据相对路径创建文件夹，并返回创建的文件夹的相对路径
    :param path:
    :param name_list:
    :return:
    """
    path_list = []
    for name in name_list:
        # print(path)
        path1 = path + name
        path_list.append(path1 + '/')
        if not os.path.exists(path1):
            os.mkdir(path1)

    return path_list
