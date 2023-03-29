## imports
import os
import numpy as np
import dlib
import cv2
import requests
from PIL import Image
from io import BytesIO


## define detector and predictor
detector = dlib.get_frontal_face_detector()  # identifies faces in images
model = 'shape_predictor_68_face_landmarks.dat'  # saved pre-trained model
predictor = dlib.shape_predictor(model)  # face landmark predictor


def finding_face(IMG_NAME):
    # entering the picture into cv2
    img = cv2.imread(os.getcwd() + "\\Uploads\\" + IMG_NAME)
    print(os.getcwd() + "\\Uploads\\" + IMG_NAME)
    # Convert into grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Load the cascade
    face_cascade = cv2.CascadeClassifier(os.getcwd() + "\\haarcascade_frontalface_alt2.xml")
    print(os.getcwd() + "\\haarcascade_frontalface_alt2.xml")

    # Detect faces
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    # Draw rectangle around the faces and crop the faces
    # Draw rectangle around the faces and crop the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
        roi_color = img[y:y + h, x:x + w]
        print("[INFO] Object found. Saving locally.")
        cv2.imshow("face", roi_color)
        img_name = os.getcwd() + "\\Faces_extract\\" + IMG_NAME[:-4]+"face" + str(x) + ".jpg"
        cv2.imwrite(img_name, roi_color)
        image_array = fetch_image(img_name)
        get_landmarks(image_array)


    # Display the output
    cv2.imwrite(os.getcwd() + "\\IMG_detect\\" + IMG_NAME + 'detcted.jpg', img)
    cv2.imshow('img', img)
    cv2.waitKey()


# fetch image from file path to the system
def fetch_image(file_path):
    """Returns numpy array for image at file_path"""
    img = Image.open(file_path)
    return cv2.cvtColor(np.array(img, np.uint8), cv2.COLOR_RGB2BGR)


def get_landmarks(image):
    """Displays 68 landmarks of each face detected in image"""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # grayscale image
    rectangles = detector(gray, 1)  # rectangles enclosing faces
    for rect in rectangles:
        points = predictor(gray, rect)  # Get the landmark points
        points_np = np.zeros((68, 2), dtype="int")
        for i in range(0, 68):
            points_np[i] = (points.part(i).x, points.part(i).y)
        points = points_np  # landmarks as 88 x 2 array
        for i, (x, y) in enumerate(points):
            cv2.circle(image, (x, y), 1, (0, 0, 255), -1)  # mark landmarks
    print(f'Image with keypoints:')
    show(image)


def show(image, scale=False):
    """Displays image with face landmarks"""
    f = 1
    if scale:
        f = 1000 / image.shape[1]
    dim = (int(image.shape[1] * f), int(image.shape[0] * f))
    resized = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
    cv2.imshow("face",resized)
    cv2.waitKey()


if __name__ == '__main__':
    # replace 'image_url' with the local file path
    finding_face("abba.jpg")

    # image_array = fetch_image("C:\\Users\\User\\Documents\\winter2023\\capstone\\FaceRecognition\\Faces_extract\\abba_face312.jpg")
    #
    # get_landmarks(image_array)
