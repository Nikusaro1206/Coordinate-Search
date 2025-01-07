import cv2
import numpy as np
import statistics

# 画像を読み込む
image = cv2.imread("testbad.jpg")
height = image.shape[0]
width = image.shape[1]

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# エッジ検出
edges = cv2.Canny(gray, 100, 400, apertureSize=3)

# Hough Line Transformで直線を検出
lines = cv2.HoughLines(edges, 1, np.pi / 180, 150)
#lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 100, minLineLength=50, maxLineGap=10)
#if lines is not None:
#    for line in lines:
#        x1, y1, x2, y2 = line[0]
#        angle = np.degrees(np.arctan2(y2 - y1, x2 - x1))
#        if -10 < angle < 10:  # 横線のみ
#            print(f"横線の角度: {angle:.2f}度")

# 横線の角度を収集
angles = []
if lines is not None:
    for rho, theta in lines[:, 0]:
        # 角度をラジアンから度に変換し、90度基準で調整
        angle = np.degrees(theta) - 90
        # 横線（水平線）に近い角度のみ収集
        if -10 < angle < 10:  # 横線の範囲を指定（例: -10°～10°）
            angles.append(angle)

# 角度を計算
if len(angles) > 0:
#    mean_angle = np.mean(angles)#平均角度
    mean_angle = statistics.median(angles)#中央値
else:
    mean_angle = 0  # 横線が見つからない場合

print(f"傾き角度: {mean_angle:.2f}度")

# 傾きを補正して画像を回転
(h, w) = image.shape[:2]
center = (w // 2, h // 2)
M = cv2.getRotationMatrix2D(center, mean_angle, 1.0)
rotated = cv2.warpAffine(image, M, (w, h))

height_coefficient = height/700
width_coefficient = width/500
resize_image = cv2.resize(rotated,(int(width/width_coefficient),int(height/height_coefficient)))
resize_edges = cv2.resize(edges,(int(width/width_coefficient),int(height/height_coefficient)))

# 結果を表示
cv2.imshow("Original Image", resize_edges)
cv2.imshow("Corrected Image", resize_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
