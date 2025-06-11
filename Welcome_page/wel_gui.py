from pathlib import Path
import subprocess
import sys
from tkinter import Tk, Canvas, Button, PhotoImage


#outer path - where this code is
#assets path - used to access the images
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"/Users/vipinchoudhary/Desktop/MediVerse/welcome_page/build/assets/frame0")


#takes ex image_1.png and combines with the assets path to give full path to loading part
def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


#runs another python file
#destroy closes this one 
def open_new_gui():
    subprocess.Popen([sys.executable, "/Users/vipinchoudhary/Desktop/MediVerse/Login_page/log_gui.py"])
    window.destroy()


#creates main window and set size and colour
window = Tk()
window.geometry("1100x733")
window.configure(bg="#FFFFFF")


#drawing area which i used on figma
canvas = Canvas(window,bg="#FFFFFF",height=733,width=1100,bd=0,highlightthickness=0,relief="ridge")
canvas.place(x=0, y=0)


# loading and positioning of the main welcome wallpaper
image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(550.0,366.0,image=image_image_1)


# for maid by vipin choudhary text and positioning
canvas.create_text(15.0,694.0,anchor="nw",text="Made By - Vipin Choudhary",fill="#FFFFFF",font=("Inter", 16 * -1))


# load button image 
# button is given command to open next python gui code
button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=open_new_gui,  
    relief="flat"
)
button_1.place(x=902.0,y=586.0,width=155.0,height=108.0)


# loading and positioning of the logo
image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(117.0,98.0,image=image_image_2)


# starts the gui and keep it running
window.mainloop()