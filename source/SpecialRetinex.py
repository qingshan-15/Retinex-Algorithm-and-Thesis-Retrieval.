import cv2
import numpy as np

from util import ImageUtil as iu


def this_retinex(img, sigma_list, a=0.000001, d=2):
    """
    复现论文的算法
    :param img:
    :param sigma_list:
    :param a: 增加值定义，为了避免0引起的对数异常值-inf或者nan
    :param d: 调节参数
    :return:
    """
    # 避免出现除0的情况
    np.seterr(divide='ignore', invalid='ignore')
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 图像的尺寸大小
    m = img.shape[0]
    n = img.shape[1]

    # 预增强图像
    # 求解最大光照点：灰度图像最大值就是最大光照点
    img_gray_max = np.max(img_gray)

    img_gray_log_sum = 0

    for i in range(m):
        for j in range(n):
            img_gray_log_sum = img_gray_log_sum + np.log(img_gray[i, j] + a)

    img_gray_avg = np.exp(img_gray_log_sum / (m * n))  # 灰度平均值

    ec = np.double(np.zeros_like(img_gray))  # 光照增强之后与原灰度图像之间的比例
    img_gray_improve = np.double(np.zeros_like(img_gray))  # 光照增强之后的图像
    for i in range(m):
        for j in range(n):
            img_gray_improve[i, j] = np.log((img_gray[i, j] / img_gray_avg) + 1) / \
                np.log((img_gray_max / img_gray_avg) + 1)
            ec[i, j] = img_gray_improve[i, j] / (img_gray[i, j] + a)

    img_b, img_g, img_r = iu.split(img)
    img_pre_b = np.multiply(ec, img_b)
    img_pre_g = np.multiply(ec, img_g)
    img_pre_r = np.multiply(ec, img_r)

    # img_new = cv2.merge([img_new_b, img_new_g, img_new_r])

    # R通道MSR
    r_out = np.double(np.zeros(shape=(m, n)))
    for sigma in sigma_list:
        r_out += np.log(img_pre_r + 1) - np.log(iu.convolution(img_pre_r, iu.gaussian(sigma)) + 1)

    r_out /= len(sigma_list)

    # R通道量化
    r_out_mean = np.mean(r_out)  # 预处理图像经过MSR处理后r通道均值
    r_out_square_sum = np.double(0)

    for i in range(m):
        for j in range(n):
            r_out_square_sum += np.square(r_out[i, j] - r_out_mean)

    r_out_v = np.sqrt(r_out_square_sum / (m * n))  # r通道均方差
    mini = np.abs(r_out_mean - d * r_out_v)
    maxi = r_out_mean + d * r_out_v

    # 量化到[0, 255]需要保证最小值为0最大值为255，否者就无法正常显示
    r_out_new = np.uint8(np.minimum(np.maximum(((r_out - mini) / (maxi - mini)) * 255, 0), 255))
    rc = np.double(r_out_new) / r_out

    # GB通道量化[0, 255]
    g_out = np.multiply(img_pre_g, rc)
    b_out = np.multiply(img_pre_b, rc)
    out_new = np.dstack([b_out, g_out, r_out_new])
    out_new = np.uint8(np.minimum(np.maximum(out_new, 0), 255))
    return out_new


# if __name__ == '__main__':
#     img = cv2.imread('../data/origin/room_out.png')
#     out = thisRetinex(img, [15, 80, 250])
#     cv2.imshow('out', out)
#     cv2.waitKey()
#     cv2.destroyAllWindows()
