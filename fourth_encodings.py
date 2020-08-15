import face_recognition


img = face_recognition.load_image_file('./imgs/crowd01.jpg')
encodings = face_recognition.face_encodings(img)
print(encodings)