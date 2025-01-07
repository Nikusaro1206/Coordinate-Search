import cv2
import numpy as np

# 画像の読み込み
image = cv2.imread("testbed3.jpg")
height = image.shape[0]
width = image.shape[1]
height_coefficient = height/700
width_coefficient = width/500
resize_image = cv2.resize(image,(int(width/width_coefficient),int(height/height_coefficient)))

# 元画像の4つの頂点を指定（手動で指定する場合）
# 例: [(左上), (右上), (右下), (左下)]
src_points = np.array([[100, 200], [400, 200], [450, 400], [50, 400]], dtype=np.float32)

# 出力画像の座標（補正後の四角形の頂点）
dst_points = np.array([[0, 0], [300, 0], [300, 400], [0, 400]], dtype=np.float32)

# 透視変換行列を計算
M = cv2.getPerspectiveTransform(src_points, dst_points)

# 画像を変換
output = cv2.warpPerspective(resize_image, M, (300, 400))

# 結果を表示
cv2.imshow("Original Image", resize_image)
cv2.imshow("Corrected Image", output)
cv2.waitKey(0)
cv2.destroyAllWindows()


