"""
提取红色印章
"""
import cv2
import numpy as np

# 图片路径，自行添加
imgpath = r"C:\Users\9000\Desktop\ssw0001-1.jpg"
# 加载图片
image = cv2.imread(imgpath)
# 统一处理图片大小
img_w = 650 if image.shape[1] > 1000 else 400
image = cv2.resize(image, (img_w, int(img_w * image.shape[0] / image.shape[1])), interpolation=cv2.IMREAD_COLOR)
impng = cv2.cvtColor(image.copy(), cv2.COLOR_RGB2RGBA)

hue_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
low_range = np.array([130, 43, 46])
high_range = np.array([180, 255, 255])
th = cv2.inRange(hue_image, low_range, high_range)
element = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
th = cv2.dilate(th, element)
index1 = th == 255
print1 = np.zeros(impng.shape, np.uint8)
print1[:, :, :] = (255, 255, 255, 0)
print1[index1] = impng[index1]  # (0,0,255)

low_range = np.array([0, 43, 46])
high_range = np.array([9, 255, 255])
th = cv2.inRange(hue_image, low_range, high_range)
element = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
th = cv2.dilate(th, element)
index1 = th == 255
print2 = np.zeros(impng.shape, np.uint8)
print2[:, :, :] = (255, 255, 255, 0)
print2[index1] = impng[index1]

# 合并图像以增强效果
imgreal = cv2.add(print2, print1)

white_px = np.asarray([255, 255, 255, 255])
(row, col, _) = imgreal.shape
for r in range(row):
    for c in range(col):
        px = imgreal[r][c]
        if all(px == white_px):
            imgreal[r][c] = impng[r][c]

# 扩充图片防止截取部分
print4 = cv2.copyMakeBorder(imgreal, 50, 50, 50, 50, cv2.BORDER_CONSTANT, value=[255, 255, 255, 0])
print2gray = cv2.cvtColor(print4, cv2.COLOR_RGBA2GRAY)
retval, grayfirst = cv2.threshold(print2gray, 254, 255, cv2.THRESH_BINARY_INV)

element = cv2.getStructuringElement(cv2.MORPH_RECT, (22, 22))
img6 = cv2.dilate(grayfirst, element)

c_canny_img = cv2.Canny(img6, 10, 10)

contours, hierarchy = cv2.findContours(c_canny_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
areas = []
for i, cnt in enumerate(contours):
    rect = cv2.minAreaRect(cnt)
    x, y, w, h = cv2.boundingRect(cnt)
    area = w * h
    ars = [area, i]
    areas.append(ars)
areas = sorted(areas, reverse=True)
print(areas)
maxares = areas[:1]

x, y, w, h = cv2.boundingRect(contours[maxares[0][1]])
print5 = print4[y:(y + h), x:(x + w)]
# 高小于宽
print(print5.shape)
if print5.shape[0] < print5.shape[1]:
    zh = int((print5.shape[1] - print5.shape[0]) / 2)
    print5 = cv2.copyMakeBorder(print5, zh, zh, 0, 0, cv2.BORDER_CONSTANT, value=[255, 255, 255, 0])
else:
    zh = int((print5.shape[0] - print5.shape[1]) / 2)
    print5 = cv2.copyMakeBorder(print5, 0, 0, zh, zh, cv2.BORDER_CONSTANT, value=[255, 255, 255, 0])
realprint = cv2.resize(print5, (150, 150))
cv2.imshow('result', realprint)
cv2.imwrite('result.png', realprint, [int(cv2.IMWRITE_JPEG_QUALITY), 95])
cv2.waitKey()
