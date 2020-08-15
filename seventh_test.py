import face_recognition
import os


def load_img(path):
    print('正在加载人员面部信息库......')
    face_lib = []
    filenamelist = []
    for dirpath, dirnames, filenames in os.walk(path):
        filenamelist.append(filenames)
        for filename in filenames:
            face_path = os.sep.join([dirpath, filename])
            face_img = face_recognition.load_image_file(face_path)
            face_encoding = face_recognition.face_encodings(face_img)[0]
            face_lib.append(face_encoding)
    return face_lib, filenamelist


face_lib, filenamelist = load_img('imgs')
print(filenamelist)


