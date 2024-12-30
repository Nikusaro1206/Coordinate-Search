import tkinter as tk
from tkinter import filedialog
import tkinter.messagebox as tkmg
import cv2
import numpy as np
from PIL import Image, ImageFilter
import os

class Seting_aplication(tk.Frame):
    def __init__(self,root=None):
        super().__init__(root,width=380,height=480,
                         borderwidth=4,relief='groove')
        self.root = root
        self.pack()
        self.pack_propagate(0)
        self.create_widgets()

    def create_widgets(self):
        #入力欄の作成
        self.input_box = tk.Entry(width=40)
        self.input_box.place(x=10, y=100)

        #ラベルの作成
        input_label = tk.Label(text="結果")
        input_label.place(x=10, y=70)

        #ボタンの作成
        button = tk.Button(text="参照",command=self.file_select)
        button.place(x=10, y=130)

        #描画開始
        Show_button =  tk.Button(text="描画",command=self.create_window)
        Show_button.place(relx=0.5,y=150,anchor=tk.CENTER)

    def file_select(self):
        idir = 'C:'
        filetype = [("jpg","*.jpg"), ("png","*.png"), ("すべて","*")]
        file_path = tk.filedialog.askopenfilename(filetypes = filetype, initialdir = idir)
        print(f"{file_path}")
        self.input_box.insert(tk.END, file_path)
    
    def create_window(self):
        current = tk.Tk()
        current.title("座標の特定")
        path = self.input_box.get
        work_window = Work_window(path=path)
        work_window.mainloop()

class Work_window(tk.Frame):
    def __init__(self,root=None,path=None):
        super().__init__(root,width=380,height=480,
                         borderwidth=4,relief='groove')
        self.root = root
        #self.pack()
        self.pack_propagate(0)
        self.create_work(path)
        
    def create_work(self,path):       
        # ウィンドウの作成
        cv2.namedWindow("Mouse Event Window")

        # コールバック関数をウィンドウにセット
        cv2.setMouseCallback("Mouse Event Window", self.mouse_callback)

        normalized_path = os.path.normpath(normalized_path)
        #画像読み込み
        img ,hsv= self.img_read(path)
        #緑の輪郭線の取得
        green_mask ,green_mask_img= self.detect_green_color(img,hsv)
        #cv2.imshow("GREEN Window", green_mask_img)
        edges,green_lines = self.edge_jadge(green_mask_img,180)

        width_x,width_y1,height_x1,height_y,width_y2,height_x2 = self.green_line_jadge(green_lines)
        filtered_green_line = np.array(self.line_jadge(width_y1,width_y2,width_x))#横の線
        filtered_green_line=np.vstack((filtered_green_line
                                    ,np.array(self.line_jadge(height_x1,height_x2,height_y))))#縦の線

        crop_img = self.img_crop(img,filtered_green_line)

        crop_hsv = cv2.cvtColor(crop_img, cv2.COLOR_BGR2HSV)
        #加工後画像処理
        #赤線(画像の拡大縮小)
        red_mask ,red_mask_img= self.detect_red_color(crop_img,crop_hsv)
        edges,red_lines = self.edge_jadge(red_mask_img,90)
        #if red_lines is not None:
        #       for line in red_lines:
        #            x1, y1, x2, y2 = line[0]# 始点と終点の座標
        #            cv2.line(crop_img, (x1, y1), (x2, y2), (0, 0, 255), 2)

        width_x,width_y1,height_x1,height_y,width_y2,height_x2 = self.green_line_jadge(red_lines)
        filtered_red_line = np.array(self.line_jadge(width_y1,width_y2,width_x))#横の線
        filtered_red_line = np.vstack((filtered_red_line
                                    ,np.array(self.line_jadge(height_x1,height_x2,height_y))))#縦の線

        #緑線再取得
        green_mask ,green_mask_img= self.detect_green_color(crop_img,crop_hsv)
        edges,green_lines = self.edge_jadge(green_mask_img,180)
        #if green_lines is not None:
        #        for line in green_lines:
        #            x1, y1, x2, y2 = line[0]# 始点と終点の座標
        #            cv2.line(crop_img, (x1, y1), (x2, y2), (0, 255, 0), 2)

        width_x,width_y1,height_x1,height_y,width_y2,height_x2 = self.green_line_jadge(green_lines)
        filtered_green_line = np.array(self.line_jadge(width_y1,width_y2,width_x))#横の線
        filtered_green_line = np.vstack((filtered_green_line
                                    ,np.array(self.line_jadge(height_x1,height_x2,height_y))))#縦の線
        for i in range (0,4):
            if i == 0:
                x1,y1,x2,y2 = filtered_green_line[0]
            elif i == 1:
                y1,x1,y2,x2 = filtered_green_line[1]
            elif i == 2:
                x1,y1,x2,y2 = filtered_red_line[0]
            elif i == 3:
                y1,x1,y2,x2 = filtered_red_line[1]
            if i == 0 or i == 1:
                cv2.line(crop_img, (x1,y1), (x2,y2), (0, 255, 0), 10)
            else:
                cv2.line(crop_img, (x1,y1), (x2,y2), (0, 0, 255), 10)
        xgap,ygap = self.red_gap(filtered_red_line,filtered_green_line)
        print(f"x:{xgap},y:{ygap}")

        output_img = self.resize_img(crop_img,xgap,ygap)

        while True:
            # ウィンドウに画像を表示
            cv2.imshow("Mouse Event Window", output_img)

            # キー入力を待機 (キー 'q' を押すと終了)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # リソースを解放
        cv2.destroyAllWindows()
    def img_read (self,path):
        img = cv2.imread(path)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        return img,hsv

    def resize_img(self,img,x,y):
        height = img.shape[0]
        width = img.shape[1]
        width_coefficient = abs(250/x)
        height_coefficient = abs(350/y)
        return cv2.resize(img,(int(width*width_coefficient),int(height*height_coefficient)))
        #return cv2.resize(img,(x,y))

    def line_jadge(self,start_point_list,end_point_list,border_point_list):
        end_point = int(np.max(border_point_list))
        start_point = int(np.min(border_point_list))
        end_median_point = int(np.median(start_point_list))
        start_median_point = int(np.median(end_point_list))
        #横線のときx1,y1,x2,y2,縦線のときy1,x1,y2,x2
        return [start_point,start_median_point,end_point,end_median_point]

    def detect_green_color(self,img,hsv):#元写真とhsv写真

        # 緑色のHSVの値域
        hsv_min = np.array([30, 64, 0])
        hsv_max = np.array([90,255,255])

        # 緑色領域のマスク（255：赤色、0：赤色以外）
        mask = cv2.inRange(hsv, hsv_min, hsv_max)

        # マスキング処理
        masked_img = cv2.bitwise_and(img, img, mask=mask)

        return mask, masked_img

    def detect_red_color(self,img,hsv):
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

    def edge_jadge (self,masked_img,angle):#angle:判定角度赤90,緑180
        # エッジ検出 (Canny)
        edges = cv2.Canny(masked_img, 150, 300)
        
        lines = cv2.HoughLinesP(edges, 1, np.pi / angle,
                            threshold=50, minLineLength=50, maxLineGap=100)
        
        return edges,lines

    def line_draw(self,img,x1,y1,x2,y2):
        pass
    def img_crop(self,img,coordinate_list):
        gap = 150
        pillow_image = Image.fromarray(img)#opencvのndarray形式をpillowの形式に変換
        pillow_x,pillow_y=pillow_image.size

        print(coordinate_list)
        height_x2 = coordinate_list[1,3]
        width_y2 = coordinate_list[0,3]
        # 切り抜く領域を指定（左, 上, 右, 下）
        crop_box= (height_x2 - gap,width_y2 - gap,pillow_x,pillow_y)# 例: (x1, y1, x2, y2)
        print(crop_box)
        cropped_image = pillow_image.crop(crop_box)
        # Pillow形式をOpenCV形式に変換
        cropped_image_cv2 = np.array(cropped_image)
        return cropped_image_cv2
        # OpenCVで切り抜き画像を保存
        #cv2.imwrite('cropped_image_cv2.jpg', cropped_image_cv2)

    def green_line_jadge(self,lines):
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
                    width_x.append(x1)
                    width_x.append(x2)
                    width_y1.append(y1)
                    width_y2.append(y2)
                elif y_range > 100 :
                    height_x1.append(x1)
                    height_x2.append(x2)
                    height_y.append(y1)
                    height_y.append(y2)
        return width_x,width_y1,height_x1,height_y,width_y2,height_x2

    def seach_red_coordinate(self,lines,type):
        if type == 0:
            pass
        elif type == 1:
            pass
        else:
            pass
        pass
    def red_gap(self,red_lines,green_lines):
        ygap = red_lines[0,3] - green_lines[0,1]
        xgap = red_lines[1,3] - green_lines[1,1]
        return xgap , ygap
    # マウスクリック時に座標を取得するコールバック関数
    def mouse_callback(self,event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:  # 左クリック時
            print(f"Clicked at: ({x}, {y})")  # 座標を表示

root = tk.Tk()
root.title("Seting Window")
app = Seting_aplication(root = root)
app.mainloop()