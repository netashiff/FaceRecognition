# imports for helping the model works properly
import os
import cv2


# this fubction will get a picture and will be able to cut the face from the IMG
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
        cv2.imwrite(os.getcwd() + "\\Faces_extract\\" + "face" + str(
            x) + ".jpg", roi_color)

    # Display the output
    cv2.imwrite(os.getcwd() + "\\IMG_detect\\" + IMG_NAME[:-4] + '_detcted.jpg', img)
    cv2.imshow('img', img)
    cv2.waitKey()


if __name__ == '__main__':
    cwd = os.getcwd()
    finding_face("abba.jpg")
