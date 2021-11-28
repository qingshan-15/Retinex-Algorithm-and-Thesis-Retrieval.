import numpy as np
import cv2


def singleScaleRetinex(img, sigma, size=0):
    """
    单尺度Retinex
    :param size: 卷积核尺寸
    :param img:
    :param sigma:
    :return:
    """
    retinex = np.log(img + 1) - np.log(cv2.GaussianBlur(img, (size, size), sigma) + 1)

    return retinex


def multiScaleRetinex(img, sigma_list, size=0):
    """
    多尺度Retinex
    :param size:
    :param img:
    :param sigma_list:
    :return:
    """
    np.seterr(divide='ignore', invalid='ignore')
    retinex = np.double(np.zeros_like(img))
    for sigma in sigma_list:
        retinex += singleScaleRetinex(img, sigma, size)

    retinex = retinex / len(sigma_list)
    # print(size)

    return retinex


def quantify(img):
    """
    将对数域图像量化到[0, 255]
    :param img:
    :return:
    """
    img_quantified = np.zeros_like(img)
    for i in range(img.shape[2]):
        img_quantified[:, :, i] = (img[:, :, i] - np.min(img[:, :, i])) / \
                        (np.max(img[:, :, i]) - np.min(img[:, :, i])) * 255

    img_quantified = np.uint8(np.minimum(np.maximum(img_quantified, 0), 255))
    return img_quantified


def MSR(img, sigma_list):
    """
    MSR算法
    :param img:
    :param sigma_list:
    :return:
    """
    img = np.double(img) + 1.0
    img_msr = np.zeros_like(img)
    for i in range(img.shape[2]):
        img_msr[:, :, i] = multiScaleRetinex(img[:, :, i] + 1.0, sigma_list)

    return quantify(img_msr)


def colorRestoration(img, alpha, beta):
    """
    色彩修复
    :param img:
    :param alpha:
    :param beta:
    :return:
    """
    img_sum = np.sum(img, axis=2, keepdims=True)

    color_restoration = beta * (np.log10(alpha * img) - np.log10(img_sum))

    return color_restoration


def simplestColorBalance(img, low_clip, high_clip):
    """
    简单色彩平衡
    :param img:
    :param low_clip:
    :param high_clip:
    :return:
    """
    total = img.shape[0] * img.shape[1]
    for i in range(img.shape[2]):
        unique, counts = np.unique(img[:, :, i], return_counts=True)
        current = 0
        for u, c in zip(unique, counts):
            if float(current) / total < low_clip:
                low_val = u
            if float(current) / total < high_clip:
                high_val = u
            current += c

        img[:, :, i] = np.maximum(np.minimum(img[:, :, i], high_val), low_val)

    return img


def MSRCR(img, sigma_list, G, b, alpha, beta, low_clip, high_clip):
    """
    MSRCR算法:Multiple Scale Retinex Color Restoration
    说明：多通道色彩恢复Retinex
    :param img:
    :param sigma_list:
    :param G:
    :param b:
    :param alpha:
    :param beta:
    :param low_clip:
    :param high_clip:
    :return:
    """
    np.seterr(divide='ignore', invalid='ignore')
    img = np.float64(img) + 1.0

    img_retinex = multiScaleRetinex(img, sigma_list)

    img_color = colorRestoration(img, alpha, beta)
    img_msrcr = G * (img_retinex * img_color + b)

    img_msrcr = simplestColorBalance(img_msrcr, low_clip, high_clip)
    img_msrcr = quantify(img_msrcr)

    return img_msrcr


def MSRCP(img, sigma_list, low_clip, high_clip):
    """
    MSRCP算法 对原来的图像进行色彩比例保存，对图像增强之后的图像进行按比例恢复
    相比MSRCR算法能够有效的避免颜色失真
    :param img:
    :param sigma_list:
    :param low_clip:
    :param high_clip:
    :return:
    """
    np.seterr(divide='ignore', invalid='ignore')
    img = np.float64(img) + 1.0

    intensity = np.sum(img, axis=2) / img.shape[2]

    retinex = multiScaleRetinex(intensity, sigma_list)

    intensity = np.expand_dims(intensity, 2)
    retinex = np.expand_dims(retinex, 2)

    intensity1 = simplestColorBalance(retinex, low_clip, high_clip)

    intensity1 = (intensity1 - np.min(intensity1)) / \
                 (np.max(intensity1) - np.min(intensity1)) * \
                 255.0 + 1.0

    img_msrcp = np.zeros_like(img)

    for y in range(img_msrcp.shape[0]):
        for x in range(img_msrcp.shape[1]):
            B = np.max(img[y, x])
            A = np.minimum(256.0 / B, intensity1[y, x, 0] / intensity[y, x, 0])
            img_msrcp[y, x, 0] = A * img[y, x, 0]
            img_msrcp[y, x, 1] = A * img[y, x, 1]
            img_msrcp[y, x, 2] = A * img[y, x, 2]

    img_msrcp = np.uint8(img_msrcp - 1.0)

    return img_msrcp

