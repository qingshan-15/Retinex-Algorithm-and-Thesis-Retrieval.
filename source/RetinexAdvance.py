import cv2
import numpy as np
import source.TraditionalRetinex as re


def logarithmicTransformation(img):
    """
    对数域变换
    :param img: 低照度图像
    :return pretreatment: 预处理之后的图像
    """
    src = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    info = src.shape
    log_sum = np.double(0)
    for i in range(info[0]):
        for j in range(info[1]):
            log_sum += np.log(np.double(src[i, j]) + 0.000001)

    p_avg = np.exp(log_sum / (info[0] * info[1]))
    (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(src)
    p0 = np.log(src/p_avg + 1) / np.log(maxVal/p_avg + 1)
    ec = p0 / (src + 0.000001)
    b, g, r = cv2.split(img)
    pretreatment = cv2.merge([ec * b, ec * g, ec * r])
    return pretreatment


def quantizedSingledMSR(img, sigma_list, d=2):
    """
    量化单通道MSR
    :param img:
    :param sigma_list:
    :param d:
    :return:
    """
    # 因为调用的是cv2中内置高斯滤波，最终结果与真实结果并不一样，即使将卷积核size作为参数传入
    rout = re.multi_scale_retinex(np.double(img), sigma_list, size=3)

    mean = np.mean(rout)

    r_sum = np.double(0)
    for i in range(rout.shape[0]):
        for j in range(rout.shape[1]):
            r_sum += np.square(rout[i, j] - mean)

    stddev = np.sqrt(r_sum / (rout.shape[0] * rout.shape[1]))
    mini = np.abs(mean - d * stddev)
    maxi = mean + d * stddev
    routnew = ((rout - mini) / (maxi - mini)) * 255
    rc = np.double(routnew) / rout
    cv2.imshow('routnew', np.uint8(np.minimum(np.maximum(routnew, 0), 255)))
    return np.uint8(np.minimum(np.maximum(routnew, 0), 255)), rc


def integration(img, sigma_list):
    """
    三通道集成
    :param img:
    :param sigma_list:
    :return:
    """
    img_pre = logarithmicTransformation(img)
    b, g, r = cv2.split(img_pre)
    routnew, ec = quantizedSingledMSR(r, sigma_list)
    bout = np.multiply(b, ec)
    gout = np.multiply(g, ec)
    img_solved = np.dstack([bout, gout, np.double(routnew)])
    return np.uint8(np.minimum(np.maximum(img_solved, 0), 255))
