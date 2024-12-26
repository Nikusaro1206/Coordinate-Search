import cv2
import numpy as np
from PIL import Image, ImageFilter

def img_read (path):
    img = cv2.imread(path)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    return img,hsv

def resize_img(img,x,y):
    #width_coefficient = 250/x
    #height_coefficient = 350/y
    #return cv2.resize(img,(int(x*width_coefficient),int(y*height_coefficient)))
    return cv2.resize(img,(x,y))

def line_jadge(start_point_list,end_point_list,border_point_list):
    end_point = int(np.max(border_point_list))
    start_point = int(np.min(border_point_list))
    end_median_point = int(np.median(start_point_list))
    start_median_point = int(np.median(end_point_list))
    #縦線のときy1,x1,y2,x2,横線のときx1,y1,x2,y2
    return [start_point,start_median_point,end_point,end_median_point]

def detect_green_color(img,hsv):#元写真とhsv写真

    # 緑色のHSVの値域1
    hsv_min = np.array([30, 64, 0])
    hsv_max = np.array([90,255,255])

    # 緑色領域のマスク（255：赤色、0：赤色以外）
    mask = cv2.inRange(hsv, hsv_min, hsv_max)

    # マスキング処理
    masked_img = cv2.bitwise_and(img, img, mask=mask)

    return mask, masked_img

def detect_red_color(img,hsv):
    # 赤色の範囲を定義（下限と上限）
    lower_red1 = np.array([0, 100, 100])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([160, 100, 100])
    upper_red2 = np.array([179, 255, 255])

    # 赤色のマスクを作成
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask = mask1 + mask2

    # マスキング処理
    masked_img = cv2.bitwise_or(img, img, mask=mask)

    return mask, masked_img

def edge_jadge (masked_img,angle):#angle:判定角度赤90,緑180
    # エッジ検出 (Canny)
    edges = cv2.Canny(masked_img, 150, 300)

    return cv2.HoughLinesP(edges, 1, np.pi / angle,
                           threshold=50, minLineLength=50, maxLineGap=100)

def line_draw(img,x1,y1,x2,y2):
    pass
def img_crop(img,coordinate_list):
    gap = 150
    pillow_image = Image.fromarray(img)#opencvのnparray形式をpillowの形式に変換
    pillow_x,pillow_y=pillow_image.size

    print(coordinate_list)
    height_x2 = coordinate_list[1,3]
    width_y2 = coordinate_list[0,3]
    # 切り抜く領域を指定（左, 上, 右, 下）
    crop_box= (height_x2 - gap,width_y2 - gap,pillow_x,pillow_y)# 例: (x1, y1, x2, y2)
    print(crop_box)
    cropped_image = pillow_image.crop(crop_box)
    # Pillow形式をOpenCV形式に変換
    #cropped_image_cv2 = cv2.cvtColor(np.array(cropped_image), cv2.COLOR_RGB2BGR)
    cropped_image_cv2 = np.array(cropped_image)
    return cropped_image_cv2
    # OpenCVで切り抜き画像を保存
    #cv2.imwrite('cropped_image_cv2.jpg', cropped_image_cv2)

def green_line_jadge(lines):
    
    #線の座標の取得
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
                #print(f'xmax:{x_range}')
                width_x.append(x1)
                width_x.append(x2)
                width_y1.append(y1)
                width_y2.append(y2)
            elif y_range > 100 :
                #print(f'ymax:{y_range}')
                height_x1.append(x1)
                height_x2.append(x2)
                height_y.append(y1)
                height_y.append(y2)
    return width_x,width_y1,height_x1,height_y,width_y2,height_x2
#画像読み込み
path = "testbed8.jpg"
img ,hsv= img_read(path)
#緑の輪郭線の取得
green_mask ,green_mask_img= detect_green_color(img,hsv)
green_lines = edge_jadge(green_mask_img,180)

width_x,width_y1,height_x1,height_y,width_y2,height_x2 = green_line_jadge(green_lines)
filtered_green_line = np.array(line_jadge(width_y1,width_y2,width_x))#横の線
filtered_green_line=np.vstack((filtered_green_line
                               ,np.array(line_jadge(height_x1,height_x2,height_y))))#縦の線

crop_img = img_crop(img,filtered_green_line)
output_img = resize_img(crop_img,500,700)
cv2.imshow("crop img", output_img)
cv2.waitKey(0)
cv2.destroyAllWindows()