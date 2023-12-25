import numpy as np
import cv2


# MSR
def replaceZeroes(data):
    min_nonzero = np.min(data[np.nonzero(data)])
    data[data == 0] = min_nonzero
    return data


def MSR(img, scales):
    weight = 1 / 3.0
    scales_size = 3

    h, w = img.shape[:2]
    dst_img = np.zeros((h, w), dtype=np.float64)
    dst_Lblur = np.zeros((h, w), dtype=np.float64)
    dst_R = np.zeros((h, w), dtype=np.float64)
    log_R = np.zeros((h, w), dtype=np.float64)

    for i in range(0, scales_size):
        img = replaceZeroes(img)
        L_blur = cv2.GaussianBlur(img, (scales[i], scales[i]), 0)
        L_blur = replaceZeroes(L_blur)
        cv2.log(img, dst_img)
        cv2.log(L_blur, dst_Lblur)
        log_R += weight * cv2.subtract(dst_img, dst_Lblur)

    cv2.normalize(log_R, dst_R, 0, 255, cv2.NORM_MINMAX)
    log_uint8 = cv2.convertScaleAbs(dst_R)

    return log_uint8


if __name__ == '__main__':
    img = cv2.imread('../data/origin/room_in.png')
    scale = [15, 80, 250]
    b, g, r = cv2.split(img)
    b_gaussian = MSR(b, scale)
    g_gaussian = MSR(g, scale)
    r_gaussian = MSR(r, scale)
    img_msr = cv2.merge([b, g, r])
    cv2.imshow('img', img)
    cv2.imshow('img msr', img_msr)
    cv2.waitKey()
