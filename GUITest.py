import tkinter as tk
from tkinter import filedialog
import tkinter.messagebox as tkmg
import cv2
import numpy as np
from PIL import Image, ImageFilter
import os
import math

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
        input_label = tk.LabelFrame(self,text="参照",padx=10,pady=10)
        input_label.place(relx=0.5,y=50,anchor=tk.CENTER)
        self.input_box = tk.Entry(self,width=40)
        self.input_box.grid(in_=input_label,row=0,column=0)
        #ボタンの作成
        button = tk.Button(self,text="参照",command=self.file_select)
        button.grid(in_=input_label,row=0,column=1)

        #設定欄の作成
        setting_sp=tk.LabelFrame(self,text="設定",padx=10,pady=10)
        setting_sp.place(relx=0.05,y=150)
        self.gap_box = tk.Entry(self,width=10)
        self.gap_box.grid(in_=setting_sp,row=0,column=0)
        self.gap_box.insert(tk.END,150)

        self.x_pixel_box = tk.Entry(self,width=10)
        self.x_pixel_box.grid(in_=setting_sp,row=1,column=0)
        self.x_pixel_box.insert(tk.END,125)
        self.y_pixel_box = tk.Entry(self,width=10)
        self.y_pixel_box.grid(in_=setting_sp,row=1,column=1)
        self.y_pixel_box.insert(tk.END,175)

        self.real_x = tk.Entry(self,width=10)
        self.real_x.grid(in_=setting_sp,row=2,column=0)
        self.real_x.insert(tk.END,500)
        self.real_y = tk.Entry(self,width=10)
        self.real_y.grid(in_=setting_sp,row=2,column=1)
        self.real_y.insert(tk.END,700)

        #描画開始
        Show_button =  tk.Button(self,text="描画",command=self.create_window)
        Show_button.place(relx=0.5,rely=0.8,anchor=tk.CENTER)

    def file_select(self):
        idir = 'C:'
        filetype = [("jpg","*.jpg"), ("png","*.png"), ("すべて","*")]
        file_path = tk.filedialog.askopenfilename(filetypes = filetype, initialdir = idir)
        #print(f"{file_path}")      
        self.input_box.delete(0,tk.END)
        self.input_box.insert(tk.END, file_path)
    
    def create_window(self):
        current = tk.Tk()
        current.title("座標の特定")
        path,gap,xpixel,ypixel,realx,realy = self.box_get()
        work_window = Work_window(root = current,path=path,gap=gap,
                                  real_x=realx,real_y=realy,x_pixel=xpixel,y_pixel=ypixel)
        work_window.mainloop()
    def box_get(self):
        path = self.input_box.get()
        gap = self.gap_box.get()
        xpixel = self.x_pixel_box.get()
        ypixel = self.y_pixel_box.get()
        realx = self.real_x.get()
        realy = self.real_y.get()

        return path,gap,xpixel,ypixel,realx,realy
class Work_window(tk.Frame):
    def __init__(self,root=None,path=None,gap=None,
                 real_x=None,real_y=None,x_pixel=None,y_pixel=None):
        super().__init__(root,width=380,height=480,
                         borderwidth=4,relief='groove')
        self.root = root
        self.pack()
        self.gap = int(gap) #切り抜き時の余白
        self.fit_x_pixel = int(x_pixel) #赤線までのピクセル数（ｘ）
        self.fit_y_pixel = int(y_pixel) #赤線までのピクセル数（ｙ）
        self.real_x = int(real_x) #赤線までの実際の長さ（ｘ，mm）
        self.real_y = int(real_y) #赤線までの実際の長さ（ｙ，mm）
        self.pixel_log = []
        self.pack_propagate(0)
        self.current_widget(path=path)

    def current_widget(self,path):
        quit_btn = tk.Button(self,text = "終了",command = self.work_destroy)
        quit_btn.place(relx=0.8,rely=0.9,anchor=tk.CENTER)

        #履歴部分
        self.rireki_sp = tk.LabelFrame(self,text="履歴",padx=10,pady=10)
        self.Text2 = tk.StringVar()
        self.Text2.set("-")
        rireki1 = tk.Message(self.rireki_sp,textvariable = self.Text2,width=270,anchor="nw")
        self.rireki_sp.place(relx=0.5,relwidth=0.3,y=220,height=150,anchor=tk.CENTER)
        rireki1.grid(in_=self.rireki_sp,row=0,column=0)
        self.create_work(path)

    def work_destroy(self):
        self.root.destroy()
        cv2.destroyAllWindows()
    
    def create_work(self,path):
        test_path = "C:\\Users\\PC-USER\\Coordinate_Search\\Coordinate-Search\\Testbed10.jpg"

        normalized_path = os.path.normpath(path)

        # ウィンドウの作成
        cv2.namedWindow(f"Mouse click window:{normalized_path}")

        # コールバック関数をウィンドウにセット
        cv2.setMouseCallback(f"Mouse click window:{normalized_path}", self.mouse_callback)
        #cv2.setMouseCallback(f"座標の特定", self.mouse_callback)

        #画像読み込み
        img ,hsv= self.img_read(normalized_path)
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
       
        width_x,width_y1,height_x1,height_y,width_y2,height_x2 = self.green_line_jadge(red_lines)
        filtered_red_line = np.array(self.line_jadge(width_y1,width_y2,width_x))#横の線
        filtered_red_line = np.vstack((filtered_red_line
                                    ,np.array(self.line_jadge(height_x1,height_x2,height_y))))#縦の線

        #緑線再取得
        green_mask ,green_mask_img= self.detect_green_color(crop_img,crop_hsv)
        edges,green_lines = self.edge_jadge(green_mask_img,180)
        
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

        # ウィンドウに画像を表示
        cv2.imshow(f"Mouse click window:{normalized_path}", output_img)

    def img_read (self,path):
        img = cv2.imread(path)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        return img,hsv

    def resize_img(self,img,x,y):

        height = img.shape[0]
        width = img.shape[1]
        width_coefficient = abs(self.fit_x_pixel/x)
        height_coefficient = abs(self.fit_y_pixel/y)
        self.x_coefficient = abs(self.real_x/self.fit_x_pixel)
        self.y_coefficient = abs(self.real_y/self.fit_y_pixel)
        
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
        
        pillow_image = Image.fromarray(img)#opencvのndarray形式をpillowの形式に変換
        pillow_x,pillow_y=pillow_image.size

        print(coordinate_list)
        height_x2 = coordinate_list[1,3]
        width_y2 = coordinate_list[0,3]
        # 切り抜く領域を指定（左, 上, 右, 下）
        crop_box= (height_x2 - self.gap,width_y2 - self.gap,pillow_x,pillow_y)# 例: (x1, y1, x2, y2)
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
    def red_gap(self,red_lines,green_lines):
        ygap = red_lines[0,3] - green_lines[0,1]
        xgap = red_lines[1,3] - green_lines[1,1]
        return xgap , ygap
    # マウスクリック時に座標を取得するコールバック関数
    def mouse_callback(self,event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:  # 左クリック時
            real_x = x*self.x_coefficient
            real_y = y*self.y_coefficient
            self.pixel_log.insert(0,(real_x,real_y))
            if len(self.pixel_log) > 1:
                x2,y2=self.pixel_log[1]
                distanse = abs(math.sqrt((real_x-x2)**2+(real_y-y2)**2))
                #check:^は「TypeError: unsupported operand type(s) for ^: 'float' and 'float'」が出て使えない
                print(f"距離:{distanse}")
                self.Text2.config(text=self.pixel_log[1:])
                #print(f"x2:{x2} y2:{y2}")
            #self.pixel_log.append(y)
            
            print(self.pixel_log[0])
            print(f"Clicked at: ({real_x}, {real_y})")  # 座標を表示

root = tk.Tk()
root.title("Seting Window")
app = Seting_aplication(root = root)
app.mainloop()