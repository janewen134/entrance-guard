import face_recognition
from PIL import Image, ImageDraw


img1 = face_recognition.load_image_file('./imgs/chenrancrowd.jpg')
img2 = face_recognition.load_image_file('./imgs/ymsingle.jpg')

encoding1 = face_recognition.face_encodings(img1)
encoding2 = face_recognition.face_encodings(img2)[0]

result = face_recognition.compare_faces(encoding1, encoding2, tolerance=0.49)

pil_img = Image.fromarray(img1)
draw_img = ImageDraw.Draw(pil_img)

locations = face_recognition.face_locations(img1)
i = 0
for t in result:
    if t:
        break
    i += 1
if i < len(locations):
    top, right, bottom, left = locations[i]
    draw_img.rectangle([(left, top), (right, bottom)], None, (0, 255, 0), 2)
    pil_img.show()
else:
    print('It\'s not in range')
