from util import PathUtil as pu

if __name__ == '__main__':
    name_list = ['1', '2', '3']
    path = '../data/'
    pu.mkdirByList(path, name_list)
