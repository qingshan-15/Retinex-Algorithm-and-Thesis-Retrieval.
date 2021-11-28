from source import TraditionalRetinex as tr
from source import SpecialRetinex as sr
from util import PathUtil as pu

import os
import cv2
import json
from matplotlib import pyplot as plt
import numpy as np

with open('resource/config.json', 'r') as f:
    config = json.load(f)

path = './data/'
path_origin = path + 'origin'
img_list = os.listdir(path_origin)
length = len(img_list)
if length == 0:
    print('空文件夹')
    exit(0)

path_list = pu.mkdirByList(path, pu.getNameWithoutSuffix(img_list))

# plt.figure()

for i in range(length):

    # 读取图像文件
    img = cv2.imread(os.path.join(path_origin, img_list[i]))

    # 处理图像文件
    # MSR方法
    img_msr = tr.MSR(img, config['sigma_list'])
    # img_msr = np.uint8(np.minimum(np.maximum(msr * 255, 0), 255))

    # MSRCR方法
    img_msrcr = tr.MSRCR(
        img,
        config['sigma_list'],
        config['G'],
        config['b'],
        config['alpha'],
        config['beta'],
        config['low_clip'],
        config['high_clip']
    )

    # MSRCP方法
    img_msrcp = tr.MSRCP(
        img,
        config['sigma_list'],
        config['low_clip'],
        config['high_clip']
    )

    # 本篇论文算法
    img_this_retinex = sr.thisRetinex(img, config['sigma_list'])

    # 保存图片处理结果，如果文件不存在，则保存在指定的文件夹下面
    if not os.path.exists(path_list[i] + 'img_msr.png'):
        cv2.imwrite(path_list[i] + 'img_msr.png', img_msr)
    if not os.path.exists(path_list[i] + 'img_msrcr.png'):
        cv2.imwrite(path_list[i] + 'img_msrcr.png', img_msrcr)
    if not os.path.exists(path_list[i] + 'img_msrcp.png'):
        cv2.imwrite(path_list[i] + 'img_msrcp.png', img_msrcp)
    if not os.path.exists(path_list[i] + 'img_this_retinex.png'):
        cv2.imwrite(path_list[i] + 'img_this_retinex.png', img_this_retinex)

    # 将图像从BGR格式转化为RGB，方便Pyplot进行整张打印输出
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    msr_rgb = cv2.cvtColor(img_msr, cv2.COLOR_BGR2RGB)
    msrcr_rgb = cv2.cvtColor(img_msrcr, cv2.COLOR_BGR2RGB)
    msrcp_rgb = cv2.cvtColor(img_msrcp, cv2.COLOR_BGR2RGB)
    this_retinex_rgb = cv2.cvtColor(img_this_retinex, cv2.COLOR_BGR2RGB)

    # pyplot打印输出
    plt.subplot(5, length, i + 1)
    plt.xticks([]), plt.yticks([])  # 去除坐标轴
    plt.imshow(img_rgb)
    plt.subplot(5, length, i + length + 1)
    plt.xticks([]), plt.yticks([])
    plt.imshow(msr_rgb)
    plt.subplot(5, length, i + length * 2 + 1)
    plt.xticks([]), plt.yticks([])
    plt.imshow(msrcr_rgb)
    plt.subplot(5, length, i + length * 3 + 1)
    plt.xticks([]), plt.yticks([])
    plt.imshow(msrcp_rgb)
    plt.subplot(5, length, i + length * 4 + 1)
    plt.xticks([]), plt.yticks([])
    plt.imshow(this_retinex_rgb)
    # plt.tight_layout()

plt.tight_layout()
plt.show()
