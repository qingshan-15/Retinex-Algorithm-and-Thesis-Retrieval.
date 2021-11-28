from source import TraditionalRetinex as tr
from util import ImageUtil as iu
import numpy as np

if __name__ == '__main__':
    kernel = iu.getKernel(15)
    print(kernel)
