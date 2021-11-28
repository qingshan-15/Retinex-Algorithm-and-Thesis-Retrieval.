from source import TraditionalRetinex as tr
import cv2

if __name__ == '__main__':
    img = cv2.imread('../data/origin/room_out.png')
    img_msr = tr.MSR(img, [15, 80, 250])
    cv2.imshow('img_msr', img_msr)
    cv2.waitKey()
    cv2.destroyAllWindows()
