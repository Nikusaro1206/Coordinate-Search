import tkinter
from tkinter import filedialog

def file_select():
  idir = 'C:'
  filetype = [("jpg","*.jpg"), ("png","*.png"), ("すべて","*")]
  file_path = tkinter.filedialog.askopenfilename(filetypes = filetype, initialdir = idir)
  input_box.insert(tkinter.END, file_path)
#ウインドウの作成
root = tkinter.Tk()
root.title("Python GUI")
root.geometry("360x240")

#入力欄の作成
input_box = tkinter.Entry(width=40)
input_box.place(x=10, y=100)

#ラベルの作成
input_label = tkinter.Label(text="結果")
input_label.place(x=10, y=70)

#ボタンの作成
button = tkinter.Button(text="参照",command=file_select)
button.place(x=10, y=130)

#ウインドウの描画
root.mainloop()