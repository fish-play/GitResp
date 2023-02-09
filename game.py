
import numpy as np

import random

import pygame


def path(H, T, t0):
    # H是我们测试模型的身高
    listy = []
    t = np.arange(0, T, t0)
    ys = H * (np.pi) / (4 * T) * np.sin(t * np.pi / T)  # 垂直方向的速度函数
    y0 = 0
    for i in ys:
        s0 = (i + y0) * t0 / 2  # 垂直方向单位时间内移动距离
        listy.append(s0)
        y0 = i  # 记录前一次的速度
    s0 = 0
    s = 0
    listy0 = []
    for i in ys:
        s = s + (i + s0) * t0 / 2  # 垂直总路程
        listy0.append(s)
        s0 = i
    y = np.array(listy0)
    x = H / 18 * (np.arctan(18 * y / H - 5) + 1.4)
    x0 = 0
    listx = []
    for i in x:
        s0 = i - x0  # 水平方向单位时间内移动距离
        listx.append(s0)
        x0 = i  # 保存前一次的X坐标
    return listx, listy


PANEL_width = 600
PANEL_highly = 500
FONT_PX = 15

pygame.init()

# 创建一个可视化窗口
winSur = pygame.display.set_mode((PANEL_width, PANEL_highly))

font = pygame.font.SysFont("123.ttf", 30)

bg_suface = pygame.Surface((PANEL_width, PANEL_highly), flags=pygame.SRCALPHA)

pygame.Surface.convert(bg_suface)

bg_suface.fill(pygame.Color(0, 0, 0, 28))

# winSur.fill((0, 0, 0))

# 数字版
# letter = [font.render(str(i), True, (0, 255, 0)) for i in range(10)]

# 字母版
letter = ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'z', 'x', 'c',
          'v', 'b', 'n', 'm']
texts = [
    font.render(str(letter[i]), True, (0, 255, 0)) for i in range(26)
]

# 按屏幕的宽带计算可以在画板上放几列坐标并生成一个列表
column = int(PANEL_width / FONT_PX)
drops = [0 for i in range(column)]
print(drops)
pan = -1
x0 = 0
y0 = 0
i0 = 0
dropsx = [0 for i in range(column)]
dropsy = [0 for i in range(column)]
listx, listy = path(400, 2, 0.1)

kk = 0  # 获取之前的坐标
finsh = False
allfinish =False
while True:
    # 从队列中获取事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.KEYDOWN:

            chang = pygame.key.get_pressed()
            if chang[32]:  # 按下空格键
                pan = 1000
                i0 = 5   # 取消密集点
    if pan > 0:
        pygame.time.delay(100)
        winSur.blit(bg_suface, (0, 0))
        pan = pan - 1
        if i0 < len(listx):
            x0 = listx[i0]
            y0 = listy[i0]
        else:
            finsh = True
        i0 = i0 + 1
        if kk == 0:
            for i in range(len(drops)):
                dropsx[i] = i * FONT_PX
                dropsy[i] = drops[i] * FONT_PX
            kk = 1

        if finsh:
            allfinish = True
            for i in range(len(drops)):
                text = random.choice(texts)
                dropsy[i] = dropsy[i] + FONT_PX
                dropsx[i] = dropsx[i]
                # 重新编辑每个坐标点的图像
                winSur.blit(text, (dropsx[i], dropsy[i]))
                if dropsy[i] > PANEL_highly and allfinish:  # 到头了
                    allfinish = True
                else:
                    allfinish =False
        for i in range(len(drops)):
            text = random.choice(texts)
            dropsy[i] = dropsy[i] + y0
            dropsx[i] = dropsx[i] + x0
            # 重新编辑每个坐标点的图像
            winSur.blit(text, (dropsx[i], dropsy[i]))
            # if drops[i] * 10 > PANEL_highly:  # 到头了，或者运气不好
            # drops[i] = 0
        if allfinish:
            pan = -1
            drops = [0 for i in range(column)]
            pygame.display.flip()
            dropsx = [0 for i in range(column)]
            dropsy = [0 for i in range(column)]
            finsh = False
            allfinish = False
            kk = 0
            continue

        pygame.display.flip()

        continue

    # 将暂停一段给定的毫秒数
    pygame.time.delay(100)

    # 重新编辑图像第二个参数是坐上角坐标
    winSur.blit(bg_suface, (0, 0))

    for i in range(len(drops)):
        text = random.choice(texts)

        # 重新编辑每个坐标点的图像

        winSur.blit(text, (i * FONT_PX, drops[i] * FONT_PX))

        drops[i] += 1  # 向下走一格
        if drops[i] * 10 > PANEL_highly or random.random() > 0.98:  # 到头了，或者运气不好
            drops[i] = 0

    pygame.display.flip()
