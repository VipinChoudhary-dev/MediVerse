import os
import threading
import numpy as np
import librosa
import tensorflow as tf
import pyaudio
from tkinter import Tk, Canvas, PhotoImage
from pathlib import Path


SAMPLE_RATE   = 24000
MODEL_PATH    = "/Users/vipinchoudhary/Desktop/MediVerse/Speech_Emotion_Detection/vip.h5"
EMOTIONS      = ['neutral', 'happy', 'sad', 'angry']

EMO_STYLE = {
    'neutral': ('#B0B0B0', '😐'),
    'happy':   ('#FFD700', '😊'),
    'sad':     ('#1E90FF', '😢'),
    'angry':   ('#FF4500', '😠'),
}
OUTPUT_PATH   = Path(__file__).parent
ASSETS_PATH   = OUTPUT_PATH / Path(r"/Users/vipinchoudhary/Desktop/MediVerse/Speech_Emotion_Detection/build/assets/frame0")


model = tf.keras.models.load_model(MODEL_PATH)


def extract_features_from_buffer(audio_data):
    signal = librosa.util.normalize(audio_data)
    signal, _ = librosa.effects.trim(signal, top_db=20)
    if len(signal) == 0:
        signal = np.zeros(4096 * 3)
    mfccs = librosa.feature.mfcc(
        y=signal, sr=SAMPLE_RATE,
        n_mfcc=40, n_fft=2048, hop_length=512
    )
    delta = librosa.feature.delta(mfccs)
    combined = np.concatenate([mfccs, delta], axis=0)
    if combined.shape[1] < 100:
        combined = np.pad(combined, ((0,0),(0,100-combined.shape[1])))
    else:
        combined = combined[:, :100]
    return combined.T


def start_live_prediction():
    p = pyaudio.PyAudio()
    stream = p.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=SAMPLE_RATE,
        input=True,
        frames_per_buffer=4096
    )
    while True:
        frames = []
        for _ in range(int(SAMPLE_RATE / 4096 * 3)):
            try:
                chunk = stream.read(4096, exception_on_overflow=False)
            except OSError:
                continue
            frames.append(chunk)
        if not frames:
            continue

        audio = np.frombuffer(b''.join(frames), np.int16).astype(np.float32)
        if np.sqrt(np.mean(audio**2)) < 100:
            emotion = 'neutral'
        else:
            feats = extract_features_from_buffer(audio)
            pred = model.predict(feats[np.newaxis, ...], verbose=0)
            emotion = EMOTIONS[np.argmax(pred)]
  
        window.after(0, update_indicator, emotion)


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def update_indicator(emotion):
    color, emoji = EMO_STYLE[emotion]
    canvas.itemconfig(indicator, fill=color)
    canvas.itemconfig(emo_text, text=f"{emoji}\n{emotion.capitalize()}")


window = Tk()
window.geometry("1100x733")
window.configure(bg="#FFFFFF")


canvas = Canvas(
    window, bg="#FFFFFF",
    height=733, width=1100,
    bd=0, highlightthickness=0, relief="ridge"
)
canvas.place(x=0, y=0)


img1 = PhotoImage(file=relative_to_assets("image_1.png"))
canvas.create_image(550, 366, image=img1)
canvas.create_text(
    124, 117, anchor="nw",
    text="SPEECH\nEMOTION\nRECOGNIZER",
    fill="#FFFFFF", font=("IBMPlexMono Bold", -48)
)

img2 = PhotoImage(file=relative_to_assets("image_2.png"))
canvas.create_image(171, 624, image=img2)
center_x, center_y = 600, 366    #
radius = 150                      


x0, y0 = center_x - radius, center_y - radius
x1, y1 = center_x + radius, center_y + radius
indicator = canvas.create_oval(
    x0, y0, x1, y1,
    fill=EMO_STYLE['neutral'][0],
    outline=""
)

# Place the emoji + label in the center
emo_text = canvas.create_text(
    center_x, center_y,
    text=f"{EMO_STYLE['neutral'][1]}\nNeutral",
    font=("Helvetica", 32),
    fill="white",
    justify="center"
)

# start prediction in background
threading.Thread(target=start_live_prediction, daemon=True).start()

window.mainloop()
