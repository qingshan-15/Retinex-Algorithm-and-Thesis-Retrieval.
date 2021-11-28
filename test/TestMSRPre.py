import source.RetinexAdvance as ra
import cv2

if __name__ == '__main__':
    img = cv2.imread('../data/origin/room_in.png')
    img_pre = ra.logarithmicTransformation(img)
    b, g, r = cv2.split(img_pre)
    sigma_list = [15, 80, 250]
    bout = ra.quantizedSingledMSR(b, sigma_list)
    gout = ra.quantizedSingledMSR(g, sigma_list)
    rout = ra.quantizedSingledMSR(r, sigma_list)
    img_merge = cv2.merge([bout, gout, rout])
    cv2.imshow('img_merge', img_merge)
    cv2.waitKey()
    cv2.destroyAllWindows()
