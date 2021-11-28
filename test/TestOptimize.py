import source.TraditionalRetinex as re
import source.RetinexAdvance as ra
import cv2

if __name__ == '__main__':
    img = cv2.imread('../data/origin/room_out.png')
    img_pre = ra.logarithmicTransformation(img)
    cv2.imshow('pre', img_pre)
    # img_gaussian = re.multiScaleRetinex(img_pre, [15, 80, 250])
    # cv2.imshow('img_gaussian', img_gaussian)
    b, g, r = cv2.split(img_pre)
    cv2.imshow('pre_r', r)
    # r_gaussian = re.multiScaleRetinex(r, [15, 80, 250])
    # cv2.imshow('r_gaussian', r_gaussian)
    img_suc = ra.integration(img, [15, 80, 250])
    cv2.imshow('img_suc', img_suc)
    cv2.waitKey()
    cv2.destroyAllWindows()
