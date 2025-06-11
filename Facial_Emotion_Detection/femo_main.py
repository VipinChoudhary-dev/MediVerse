import cv2
import numpy as np
from deepface import DeepFace

# blueprint
face_model_proto = "/Users/vipinchoudhary/Desktop/MediVerse/Facial_Emotion_Detection/arch.vip"
face_model_weights = "/Users/vipinchoudhary/Desktop/MediVerse/Facial_Emotion_Detection/lesgo.vip"
face_net = cv2.dnn.readNetFromCaffe(face_model_proto, face_model_weights)

# for starting the webcam
cap = cv2.VideoCapture(0)

# dict that links each emotion to a colour
emotion_styles = {
    'angry':    {'color': (0, 0, 255)},
    'disgust':  {'color': (0, 102, 0)},
    'fear':     {'color': (255, 255, 0)},
    'happy':    {'color': (0, 255, 255)},
    'sad':      {'color': (255, 0, 0)},
    'surprise': {'color': (128, 0, 128)},
    'neutral':  {'color': (192, 192, 192)}
}

# a loop for processing each frame captured by webcam untils someone stops it
while True:
    success, frame = cap.read()
    if not success:
        break

    frame_height, frame_width = frame.shape[:2]

    # preparing frame for face detection
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0,
                                 (300, 300), (104.0, 177.0, 123.0))
    # blob fed to face detection model
    face_net.setInput(blob)
    # detection runs the model and now contains many face detections
    detections = face_net.forward()

    # it pinpoints the face of the user
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.5:
            box = detections[0, 0, i, 3:7] * np.array([frame_width, frame_height, frame_width, frame_height])
            x1, y1, x2, y2 = box.astype("int")
            x1, y1 = max(0, x1), max(0, y1)
            x2, y2 = min(frame_width - 1, x2), min(frame_height - 1, y2)

            # cuts the face from the frame
            face_crop = frame[y1:y2, x1:x2]
            if face_crop.size == 0:
                continue

            # analyzes the emotion
            try:
                face_rgb = cv2.cvtColor(face_crop, cv2.COLOR_BGR2RGB)
                analysis = DeepFace.analyze(face_rgb, actions=['emotion'], enforce_detection=False, silent=True)

                dominant_emotion = analysis[0]['dominant_emotion']
                emotion_scores = analysis[0]['emotion']

                # draws a colour around the face
                if dominant_emotion in emotion_styles:
                    color = emotion_styles[dominant_emotion]['color']
                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 3)

                    # bar graph for all emotions
                    for idx, (emotion, score) in enumerate(emotion_scores.items()):
                        bar_x, bar_y = 10, 40 + idx * 35
                        bar_length = int(score * 2)
                        bar_color = emotion_styles.get(emotion, {'color': (200, 200, 200)})['color']

                        cv2.rectangle(frame, (bar_x, bar_y),
                                      (bar_x + bar_length, bar_y + 20), bar_color, -1)
                        cv2.putText(frame, f"{emotion}: {score:.1f}%",
                                    (bar_x + 210, bar_y + 15), cv2.FONT_HERSHEY_SIMPLEX,
                                    0.55, (255, 255, 255), 1, cv2.LINE_AA)

            except Exception as e:
                print(f"Emotion analysis error: {e}")

    # adding title to frame
    title = "Live Emotion Detection"
    cv2.putText(frame, title, (10, 35), cv2.FONT_HERSHEY_COMPLEX, 1.0,
                (0, 0, 0), 3, cv2.LINE_AA)
    cv2.putText(frame, title, (10, 35), cv2.FONT_HERSHEY_COMPLEX, 1.0,
                (255, 255, 255), 1, cv2.LINE_AA)

    cv2.imshow('Emotion AI Display', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()# turn webcam off
cv2.destroyAllWindows()# close the window
