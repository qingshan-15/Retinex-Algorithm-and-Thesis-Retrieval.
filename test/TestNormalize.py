import cv2
import source.RetinexAdvance as ra

if __name__ == '__main__':
    img = cv2.imread('../data/origin/room_in.png')
    img_pre = ra.logarithmicTransformation(img)
    b, g, r = cv2.split(img_pre)
    cv2.imshow('pre_r', r)
    r_normalize = cv2.normalize(r)
