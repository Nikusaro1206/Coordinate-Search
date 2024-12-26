import cv2
import numpy as np

image = cv2.imread("testbed7.jpg")
height = image.shape[0]
width = image.shape[1]
height_coefficient = height/700
width_coefficient = width/500

output_image = cv2.resize(image,(int(width/width_coefficient),int(height/height_coefficient)))
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
resize_hsv = cv2.resize(hsv,(int(width/width_coefficient),int(height/height_coefficient)))

# 緑色の範囲を指定
lower_green = np.array([30, 64, 0])  # 下限
upper_green = np.array([90, 255, 255])  # 上限

mask = cv2.inRange(hsv, lower_green, upper_green)
masked_img = cv2.bitwise_and(image,image,mask=mask)
resize_mask = cv2.resize(masked_img,(int(width/width_coefficient),int(height/height_coefficient)))

# エッジ検出 (Canny)
edges = cv2.Canny(masked_img, 150, 300)
resize_edges = cv2.resize(edges,(int(width/width_coefficient),int(height/height_coefficient)))

lines = cv2.HoughLinesP(edges, 1, np.pi / 180,threshold=50, minLineLength=50, maxLineGap=100)

width_x = []
width_y1 = []
height_x1 = []
height_y = []
width_y2 = []
height_x2 = []
if lines is not None:
    for line in lines:
        x1, y1, x2, y2 = line[0]  # 始点と終点の座標
        x_range = abs(x2-x1)
        y_range = abs(y2-y1)
        
        if x_range > 100 :
            print(f'xmax:{x_range}')
            width_x.append(x1)
            width_x.append(x2)
            width_y1.append(y1)
            width_y2.append(y2)
        elif y_range > 100 :
            print(f'ymax:{y_range}')
            height_x1.append(x1)
            height_x2.append(x2)
            height_y.append(y1)
            height_y.append(y2)

#横線を描画
width_max_x = np.max(width_x)
width_min_x = np.min(width_x)
width_mean_y1 = np.median(width_y1)
width_mean_y2 = np.median(width_y2)
output_x1 = int(width_min_x/width_coefficient)
output_y1 = int(width_mean_y1/height_coefficient)
output_x2 = int(width_max_x/width_coefficient)
output_y2 = int(width_mean_y2/height_coefficient)
print(f"Line detected: Start ({output_x1}, {output_y1}), End ({output_x2}, {output_y2})")
# 線を描画
cv2.line(output_image, (output_x1,output_y1), (output_x2,output_y2), (0, 255, 0), 2)

#縦線を描画
height_max_y = np.max(height_y)
height_min_y = np.min(height_y)
height_mean_x1 = np.median(height_x1)
height_mean_x2 = np.median(height_x2)
output_x1 = int(height_mean_x1/width_coefficient)
output_y1 = int(height_min_y/height_coefficient)
output_x2 = int(height_mean_x2/width_coefficient)
output_y2 = int(height_max_y/height_coefficient)
print(f"Line detected: Start ({output_x1}, {output_y1}), End ({output_x2}, {output_y2})")
# 線を描画
cv2.line(output_image, (output_x1,output_y1), (output_x2,output_y2), (0, 255, 0), 2)

# 結果を表示
#cv2.imshow("resize mask", resize_mask)
#cv2.imshow("resize hsv", resize_hsv)
#cv2.imshow("resize Lines", masked_img)
cv2.imshow("Detected Lines", output_image)
cv2.imshow("Edge Lines", resize_edges)
cv2.waitKey(0)
cv2.destroyAllWindows()