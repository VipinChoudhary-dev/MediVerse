from pathlib import Path
import subprocess
import sys
from tkinter import Tk, Canvas, Button, PhotoImage


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"/Users/vipinchoudhary/Desktop/MediVerse/section_page/build/assets/frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def open_new_gui_1():
    window.iconify()  
    subprocess.Popen([sys.executable, "/Users/vipinchoudhary/Desktop/MediVerse/Dashboard_page/dash_main.py"])

def open_new_gui_2():
    window.iconify()
    subprocess.Popen([sys.executable, "/Users/vipinchoudhary/Desktop/MediVerse/Video_page/video_main.py"])
    
def open_new_gui_3():
    window.iconify()
    subprocess.Popen([sys.executable, "/Users/vipinchoudhary/Desktop/MediVerse/Medical_Chatbot/chat_main.py"])
    
def open_new_gui_4():
    window.iconify()
    subprocess.Popen([sys.executable, "/Users/vipinchoudhary/Desktop/MediVerse/Facial_Emotion_Detection/femo_main.py"])
    
def open_new_gui_5():
    window.iconify()
    subprocess.Popen([sys.executable, "/Users/vipinchoudhary/Desktop/MediVerse/Speech_Emotion_Detection/semo_main.py"])


window = Tk()
window.geometry("1100x733")
window.configure(bg="#FFFFFF")


canvas = Canvas(
    window,
    bg="#FFFFFF",
    height=733,
    width=1100,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)
canvas.place(x=0, y=0)


image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
canvas.create_image(550.0, 366.0, image=image_image_1)


button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
Button(image=button_image_1, borderwidth=0, highlightthickness=0,
       command=open_new_gui_5, relief="flat")\
    .place(x=653.0, y=536.0, width=324.0, height=95.0)

button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
Button(image=button_image_2, borderwidth=0, highlightthickness=0,
       command=open_new_gui_3, relief="flat")\
    .place(x=388.0, y=370.0, width=324.0, height=95.0)

button_image_3 = PhotoImage(file=relative_to_assets("button_3.png"))
Button(image=button_image_3, borderwidth=0, highlightthickness=0,
       command=open_new_gui_1, relief="flat")\
    .place(x=123.0, y=205.0, width=324.0, height=95.0)

button_image_4 = PhotoImage(file=relative_to_assets("button_4.png"))
Button(image=button_image_4, borderwidth=0, highlightthickness=0,
       command=open_new_gui_4, relief="flat")\
    .place(x=123.0, y=539.0, width=324.0, height=92.0)

button_image_5 = PhotoImage(file=relative_to_assets("button_5.png"))
Button(image=button_image_5, borderwidth=0, highlightthickness=0,
       command=open_new_gui_2, relief="flat")\
    .place(x=653.0, y=205.0, width=324.0, height=95.0)


canvas.create_text(
    320.0, 47.0, anchor="nw",
    text="MEDIVERSE",
    fill="#FFFFFF",
    font=("Roboto CondensedBold", -80)
)


image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
canvas.create_image(987.0, 99.0, image=image_image_2)


image_image_3 = PhotoImage(file=relative_to_assets("image_3.png"))
canvas.create_image(131.0, 414.0, image=image_image_3)


window.mainloop()
