import cv2
import numpy as np

# 画像を読み込む
image = cv2.imread("red_line_image.jpg")

# 画像をHSV色空間に変換
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

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
edges = cv2.Canny(mask, 50, 150)

# 線を検出 (Hough Line Transform)
lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=50, minLineLength=50, maxLineGap=10)

# 検出された線の描画と座標の出力
if lines is not None:
    for line in lines:
        x1, y1, x2, y2 = line[0]  # 始点と終点の座標
        print(f"Line detected: Start ({x1}, {y1}), End ({x2}, {y2})")
        # 線を描画
        cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

# 結果を表示
cv2.imshow("Detected Lines", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
