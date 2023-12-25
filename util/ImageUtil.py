import numpy as np
import cv2


def split(img):
    """
    为了提升速度，直接使用数组切片对图片进行通道分离
    :param img:
    :return:
    """
    b = img[:, :, 0]
    g = img[:, :, 1]
    r = img[:, :, 2]
    return b, g, r


def gaussian(sigma, size=3):
    """
    高斯函数, 获得卷积核
    :param sigma: 高斯函数参数sigma
    :param size: 卷积核尺寸：size * size
    :return: res
    """
    kernel = np.zeros(shape=(size, size))
    for i in range(size):
        for j in range(size):
            kernel[i, j] = np.exp(-(np.square(i) + np.square(j)) / (2 * np.square(sigma))) / \
                        (2 * np.square(sigma) * np.pi)

    return kernel


def convolution(img, kernel):
    """
    高斯卷积，二维方向上的滤波其实就是卷积
    :param img: 传入的图像
    :param kernel: 需要进行卷积的核
    :return:
    """
    # 需要注意的是，img.astype(np.double)是点睛之笔，新版本的迭代不允许uint8最为参数传递
    res = cv2.filter2D(img.astype(np.double), -1, kernel, borderType=cv2.BORDER_CONSTANT)
    return res
