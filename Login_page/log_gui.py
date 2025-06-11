from pathlib import Path
import subprocess
import sys
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, messagebox


# outer path - where this code is
# assets path - used to access the images
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"/Users/vipinchoudhary/Desktop/MediVerse/Login_page/build/assets/frame0")


# takes ex image_1.png and combines with the assets path to give full path to loading part
def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


# runs another python file
# destroy closes this one
def open_new_gui():
    subprocess.Popen([sys.executable, "/Users/vipinchoudhary/Desktop/MediVerse/Section_page/sec_gui.py"])
    window.destroy()


# to confirm username and pass before opening next gui
def submit_action():
    user = entry_1.get()
    pwd = entry_2.get()
    # check if credentials match
    if user == "VIPIN" and pwd == "091105":
        open_new_gui()
    else:
        # show error message
        messagebox.showerror("Login Failed", "Invalid username or password.")


# creates main window and set size and colour
window = Tk()
window.geometry("1100x733")
window.configure(bg = "#FFFFFF")


# drawing area which i used on figma
canvas = Canvas(window,bg = "#FFFFFF",height = 733,width = 1100,bd = 0,highlightthickness = 0,relief = "ridge")
canvas.place(x = 0, y = 0)


# navy blue rectangle on which i made it
canvas.create_rectangle(550.0,0.0,1100.0,733.0,fill="#344865",outline="")
canvas.create_text(624.0,111.0,anchor="nw",text="LOGIN PAGE",fill="#FFFFFF",font=("Inter Bold", 64 * -1))


# for user id and pass text and positioning
canvas.create_text(596.0,230.0,anchor="nw",text="USER ID:",fill="#FFFFFF",font=("IBMPlexMono SemiBold", 32 * -1))
canvas.create_text(596.0,384.0,anchor="nw",text="PASSWORD:",fill="#FFFFFF",font=("IBMPlexMono SemiBold", 32 * -1))


# for user id box_image, entry & positioning
entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    819.0,
    310.5,
    image=entry_image_1
)
entry_1 = Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0,
    font=("IBMPlexMono SemiBold", 24)  # increased font size
)
entry_1.place(
    x=596.0,
    y=283.0,
    width=446.0,
    height=53.0
)


# for pass box_image, entry & positioning
entry_image_2 = PhotoImage(
    file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(
    819.0,
    464.5,
    image=entry_image_2
)
entry_2 = Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0,
    font=("IBMPlexMono SemiBold", 24),  # increased font size
    show="*"  # mask password input
)
entry_2.place(
    x=596.0,
    y=437.0,
    width=446.0,
    height=53.0
)


# for begin button
button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=submit_action,  # changed to validation function
    relief="flat"
)
button_1.place(
    x=734.0,
    y=569.0,
    width=208.0,
    height=70.0
)


# for shade over begin button
button_image_hover_1 = PhotoImage(
    file=relative_to_assets("button_hover_1.png"))

def button_1_hover(e):
    button_1.config(
        image=button_image_hover_1
    )
def button_1_leave(e):
    button_1.config(
        image=button_image_1
    )

button_1.bind('<Enter>', button_1_hover)
button_1.bind('<Leave>', button_1_leave)


# for girl doctor image
image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(275.0,366.0,image=image_image_2)


# starts the gui and keep it running
window.mainloop()
