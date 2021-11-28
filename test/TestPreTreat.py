import source.TraditionalRetinex as retinex
import source.RetinexAdvance as ra
import cv2

if __name__ == '__main__':
    img = cv2.imread("../data/origin/room_in.png")
    img_pre = ra.logarithmicTransformation(img)
    cv2.imshow('img_pre', img_pre)
    b, g, r = cv2.split(img)
    g_gaussian = retinex.multiScaleRetinex(g, [15, 80, 250])
    cv2.imshow('g_gaussian', g_gaussian)
    b_gaussian = retinex.multiScaleRetinex(b, [15, 80, 250])
    cv2.imshow('b_gaussian', g_gaussian)
    r_gaussian = retinex.multiScaleRetinex(r, [15, 80, 250])
    cv2.imshow('r_gaussian', g_gaussian)
    merge = cv2.merge([b_gaussian, g_gaussian, r_gaussian])
    cv2.imshow('merge', merge)
    cv2.waitKey()
