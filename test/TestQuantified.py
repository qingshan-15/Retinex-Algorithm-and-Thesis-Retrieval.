import source.RetinexAdvance as ra
import cv2
import numpy as np

if __name__ == '__main__':
    img = cv2.imread('../data/origin/room_out_person.png')
    img_pre = ra.logarithmicTransformation(img)
    b, g, r = cv2.split(img_pre)
    b_qun = ra.quantizedSingledMSR(b, [15, 80, 250])
    cv2.imshow('img_b', np.uint8(np.minimum(np.maximum(b_qun, 0), 255)))
    g_qun = ra.quantizedSingledMSR(g, [15, 80, 250])
    cv2.imshow('img_g', np.uint8(np.minimum(np.maximum(g_qun, 0), 255)))
    r_qun = ra.quantizedSingledMSR(r, [15, 80, 250])
    cv2.imshow('img_r', np.uint8(np.minimum(np.maximum(r_qun, 0), 255)))
    cv2.imshow('img_qua', np.uint8(np.minimum(np.maximum(cv2.merge([b_qun, g_qun, r_qun]), 0), 255)))
    cv2.waitKey()
    cv2.destroyAllWindows()
