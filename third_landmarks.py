import face_recognition
from PIL import Image, ImageDraw

img = face_recognition.load_image_file('./imgs/crowd01.jpg')
landmarks_list = face_recognition.face_landmarks(img)
locations = face_recognition.face_locations(img)

pil_img = Image.fromarray(img)
draw_pil = ImageDraw.Draw(pil_img)

facial_features = [
    'chin', 'nose_bridge', 'nose_tip', 'left_eyebrow', 'right_eyebrow', 'left_eye', 'right_eye', 'top_lip', 'bottom_lip'
]

for landmarks in landmarks_list:
    for feature in facial_features:
        draw_pil.line(landmarks[feature])
for location in locations:
    top, right, bottom, left = location
    draw_pil.rectangle([(left, top), (right, bottom)], None, (0, 255, 0), width=3)


pil_img.show()

