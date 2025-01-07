import cv2
import numpy as np
from PIL import Image
import os

A=50#どこまでの近さの線を消すか

# 画像を読み込む
#Import_photo = "C:\\Users\\PC-USER\\Coordinate_Search\\Coordinate-Search\\testbed2.jpg"
Import_photo = "testbed7.jpg"

image = cv2.imread(Import_photo)
height = image.shape[0]
width = image.shape[1]
height_coefficient = height/700
width_coefficient = width/500
output_image = cv2.resize(image,(int(width/width_coefficient),int(height/height_coefficient)))
#image2 = cv2.resize(image,(int(width),int(height)))
image2 = image

# 画像をHSV色空間に変換
hsv = cv2.cvtColor(image2, cv2.COLOR_BGR2HSV)
resize_hsv = cv2.resize(hsv,(int(width/width_coefficient),int(height/height_coefficient)))

# 赤色の範囲を定義（下限と上限）
# 赤色は2つの範囲（低周波と高周波）を考慮する必要がある
lower_red1 = np.array([0, 100, 100])
upper_red1 = np.array([10, 255, 255])
lower_red2 = np.array([160, 100, 100])
upper_red2 = np.array([179, 255, 255])

# 赤色のマスクを作成
mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
mask = cv2.bitwise_or(mask1, mask2)

# エッジ検出 (Canny)
edges = cv2.Canny(mask, 150, 500)

# 線を検出 (Hough Line Transform)
lines = cv2.HoughLinesP(edges, 1, np.pi / 90,threshold=50, minLineLength=50, maxLineGap=100)
print(lines)
x = 0#一つ前のx座標
y = 0#一つ前のy座標
B = 1#何個目の座標か
n = 1#何個目の線か

filtered_lines =[]
if lines is not None:
    for line in lines:
        x1, y1, x2, y2 = line[0]  # 始点と終点の座標
        
        if not(x - A < x1 < x + A or y -A < y1 < y - A):
            #交点の座標の特定
            if n == 1:
                origin_x = int(x1/width_coefficient)
            elif n ==2:
                origin_y = int(y1/height_coefficient)
            else:
                pass
            n = n + 1
            x = x1
x = 0
# 検出された線の描画と座標の出力
if lines is not None:
    for line in lines:
        x1, y1, x2, y2 = line[0]  # 始点と終点の座標
        
        if not(x - A < x1 < x + A or y -A < y1 < y - A):

            filtered_lines.append(line)

            output_x1 = int(x1/width_coefficient)
            output_y1 = int(y1/height_coefficient)
            output_x2 = int(x2/width_coefficient)
            output_y2 = int(y2/height_coefficient)
            print(f"Line detected: Start ({output_x1}, {output_y1}), End ({output_x2}, {output_y2})")
            # 線を描画
            cv2.line(output_image, (output_x1,output_y1), (output_x2,output_y2), (0, 255, 0), 2)
            #cv2.line(hsv, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.line(output_image,(origin_x,origin_y),(output_x1,output_y1),(0,0,255),2)
            x = x1
        else:
            pass

        
# 結果を表示
cv2.imshow("Detected Lines", output_image)
cv2.imshow("resize hsv", resize_hsv)
#cv2.imshow("Detected Lines", edges)
cv2.waitKey(0)
cv2.destroyAllWindows()