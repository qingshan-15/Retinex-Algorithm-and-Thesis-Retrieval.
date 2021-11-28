## Retinex算法复现
[参考论文 用于低照度图像增强的自适应颜色保持算法](http://cea.ceaj.org/CN/Y2019/V55/I24/190)

#### 小组成员以及职责分工

| 姓名   | 主要完成内容                             |
| ------ | ---------------------------------------- |
| 夏鑫鑫 | 参考论文的理解与细节把握，PPT讲解        |
| 李先雷 | 代码部分，调优以及整合实现，代码文档编写 |
| 张鑫玉 | 后期实验文档处理，PPT制作                |

#### 结构说明

![结构](https://gitee.com/QingShanxl/pictures/raw/master/img/image-20211127005550974.png)

#### 运行说明

1. 本次算法复现一共实现了四种算法：`MSR`，`MSRCR`，`MSRCP`，还有论文中的算法
2. 直接点击`run.py`右键运行会显示原图以及上述四种算法的运行结果
3. 运行程序的过程中，读取的图片路径为`data/origin`，然后会将最终的结果分别保存到与其文件名称相同的、不包含后缀的文件夹下面，同样也是在`data`下
4. 本次复现算法直接使用暴力遍历的方式，所以在遍历高分辨率、大尺寸图像时会出现时间过长的问题

#### 环境说明

##### 硬件环境

$$
\begin{array}{l|r}
\hline
硬件 & 型号 \\\\
\hline
中央处理器 & Intel(R)\ Core(TM)\ i5-8300H\ CPU@2.30GHz，2301 Mhz \\\\
显卡 & NVIDIA\ GeForce\ GTX\ 1050\ Ti \\\\
内存1 & Samsung\ DDR4\ 2666MHz\ 8GB \\\\
内存2 & Goldkey\ DDR4\ 2666MHz\ 8GB \\\\
\hline
\end{array}
$$

##### 软件环境(包括操作系统以及python软件包)

$$
\begin{array}{l|r}
\hline
软件 & 型号 \\\\
\hline
Windows & 教育版\ 21H1 \\\\
PyCharm\ 2020.2.3 & 202.7660.27 \\\\
Typora & 0.9.86 \\\\
python & 3.8 \\\\
pip & 21.0.1 \\\\
numpy & 1.19.2 \\\\ 
matplotlib & 3.3.4 \\\\
opencv-python & 4.5.2.54 \\\\
opencv-contrib-python & 4.5.3.56 \\\\
\hline
\end{array}
$$

#### 鸣谢

感谢牟老师和新月学姐的指导
