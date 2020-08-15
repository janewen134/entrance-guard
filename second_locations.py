import face_recognition
from PIL import Image
import cv2

img = face_recognition.load_image_file('./imgs/crowd01.jpg')
locations = face_recognition.face_locations(img)
print(locations)

for face in locations:
    top, right, bottom, left = face
    # p_img = img[top: bottom, left: right]
    # pil_img = Image.fromarray(p_img)
    # pil_img.show()
    cv2.rectangle(img, (left, top), (right, bottom), (0, 255, 0), 1)

cv2.imshow('img', img)
cv2.waitKey(0)
