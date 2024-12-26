import cv2
import numpy as np

# 画像の読み込み
image = cv2.imread("testbad.jpg")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# エッジ検出
edges = cv2.Canny(gray, 100, 400, apertureSize=3)

# Hough Line Transform
lines = cv2.HoughLines(edges, 1, np.pi / 180, 200)

angles = []
if lines is not None:
    for rho, theta in lines[:, 0]:
        angle = np.degrees(theta) - 90  # 角度を計算
        angles.append(angle)

# 傾きの平均を計算
if angles:
    mean_angle = np.mean(angles)
else:
    mean_angle = 0  # 傾きが見つからない場合は0

# 画像を回転
(h, w) = image.shape[:2]
center = (w // 2, h // 2)
M = cv2.getRotationMatrix2D(center, mean_angle, 1.0)
rotated = cv2.warpAffine(image, M, (w, h))

height = rotated.shape[0]
width = rotated.shape[1]
height_coefficient = height/700
width_coefficient = width/500
output_image = cv2.resize(rotated,(int(width/width_coefficient),int(height/height_coefficient)))
output_edges = cv2.resize(edges,(int(width/width_coefficient),int(height/height_coefficient)))


# 結果を表示
cv2.imshow("Rotated Image", output_image)
cv2.imshow("edge Image", output_edges)
cv2.waitKey(0)
cv2.destroyAllWindows()