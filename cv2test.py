import cv2
import numpy as np

# マウスクリック時に座標を取得するコールバック関数
def mouse_callback(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:  # 左クリック時
        print(f"Clicked at: ({x}, {y})")  # 座標を表示

# ウィンドウの作成
cv2.namedWindow("Mouse Event Window")

# コールバック関数をウィンドウにセット
cv2.setMouseCallback("Mouse Event Window", mouse_callback)

# 画像を読み込んでbgr2rgb変換
file_path = "C:\\Users\\PC-USER\\Downloads\\mouseclicktestimag.jpg"
image_bgr = cv2.imread(file_path)
image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)

while True:
    # ウィンドウに画像を表示
    cv2.imshow("Mouse Event Window", image_bgr)

    # キー入力を待機 (キー 'q' を押すと終了)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# リソースを解放
cv2.destroyAllWindows()
