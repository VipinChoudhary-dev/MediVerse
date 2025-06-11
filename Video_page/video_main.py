from pathlib import Path
import webbrowser  # to open youtube links
from tkinter import Tk, Canvas, Button, PhotoImage


youtube_links = [
    "https://www.youtube.com/watch?v=G3Djx-0IX_M",
    "https://www.youtube.com/watch?v=ahwNqYC2txA",
    "https://www.youtube.com/watch?v=h59tggVqGfg",
    "https://www.youtube.com/watch?v=Fnt8jv1uf3Q",
    "https://www.youtube.com/watch?v=Wd4qS6_ETPs",
    "https://www.youtube.com/watch?v=auogbJFitmI&t=66s",
]


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"/Users/vipinchoudhary/Desktop/MediVerse/Video_page/build/assets/frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


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


# background image
image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
canvas.create_image(550.0, 366.0, image=image_image_1)


# Button 1
button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda url=youtube_links[0]: webbrowser.open(url),
    relief="flat"
)
button_1.place(x=653.0, y=536.0, width=324.0, height=95.0)


# Button 2
button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda url=youtube_links[1]: webbrowser.open(url),
    relief="flat"
)
button_2.place(x=123.0, y=369.0, width=324.0, height=95.0)


# Button 3
button_image_3 = PhotoImage(file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=lambda url=youtube_links[2]: webbrowser.open(url),
    relief="flat"
)
button_3.place(x=653.0, y=369.0, width=324.0, height=95.0)


# Button 4
button_image_4 = PhotoImage(file=relative_to_assets("button_4.png"))
button_4 = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    command=lambda url=youtube_links[3]: webbrowser.open(url),
    relief="flat"
)
button_4.place(x=123.0, y=205.0, width=324.0, height=95.0)


# Button 5
button_image_5 = PhotoImage(file=relative_to_assets("button_5.png"))
button_5 = Button(
    image=button_image_5,
    borderwidth=0,
    highlightthickness=0,
    command=lambda url=youtube_links[4]: webbrowser.open(url),
    relief="flat"
)
button_5.place(x=123.0, y=539.0, width=324.0, height=92.0)


# Button 6
button_image_6 = PhotoImage(file=relative_to_assets("button_6.png"))
button_6 = Button(
    image=button_image_6,
    borderwidth=0,
    highlightthickness=0,
    command=lambda url=youtube_links[5]: webbrowser.open(url),
    relief="flat"
)
button_6.place(x=653.0, y=205.0, width=324.0, height=95.0)


# Title text
canvas.create_text(
    262.0,
    47.0,
    anchor="nw",
    text="VIDEO LIBRARY",
    fill="#FFFFFF",
    font=("Roboto CondensedBold", 80 * -1)
)


# for the logo image
image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
canvas.create_image(
    987.0,
    99.0,
    image=image_image_2
)


window.mainloop()
