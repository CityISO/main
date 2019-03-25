import cv2
import numpy as np
from keras.models import load_model
from utils.datasets import get_labels
from utils.inference import apply_offsets
from utils.preprocessor import preprocess_input


EMOTION_MODEL_PATH = './models/emotion_model.hdf5'
EMOTION_LABELS = get_labels('fer2013')
EMOTION_OFFSETS = (20, 40)
FACE_CASCADE = cv2.CascadeClassifier('./models/haarcascade_frontalface_default.xml')
EMOTION_CLASSIFIER = load_model(EMOTION_MODEL_PATH)
EMOTION_TARGET_SIZE = EMOTION_CLASSIFIER.input_shape[1:3]


def get_emotions(bgr_image):
    gray_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2GRAY)
    faces = FACE_CASCADE.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5,
         minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)
    if not len(faces):
        print('Array is empty')
        return -1
    result = []
    for face_coordinates in faces:
        x_1, x_2, y_1, y_2 = apply_offsets(face_coordinates, EMOTION_OFFSETS)
        gray_face = gray_image[y_1:y_2, x_1:x_2]
        try:
            gray_face = cv2.resize(gray_face, EMOTION_TARGET_SIZE)
        except:
            # TODO: handle errors
            continue

        gray_face = preprocess_input(gray_face, True)
        gray_face = np.expand_dims(gray_face, 0)
        gray_face = np.expand_dims(gray_face, -1)
        emotion_prediction = EMOTION_CLASSIFIER.predict(gray_face)
        emotion_probability = np.max(emotion_prediction)
        emotion_label_arg = np.argmax(emotion_prediction)
        emotion_text = EMOTION_LABELS[emotion_label_arg]
        print(f"{emotion_label_arg} {emotion_text}: {round(emotion_probability * 100, 1)}%")
        if emotion_probability > 0.5:
            result.append(emotion_label_arg)
    return np.mean(result) if result else -1


def get_emotions_from_image(path):
    image = cv2.imread(path)
    return get_emotions(image)
