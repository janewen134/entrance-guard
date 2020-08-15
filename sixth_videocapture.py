import cv2
from PIL import Image, ImageDraw
import numpy

capture = cv2.VideoCapture(0)

while True:
    ret, frame = capture.read()
    if ret:
        img_pil = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        draw_img = ImageDraw.Draw(img_pil)
        draw_img.text((100, 100), 'test', fill=(0, 0, 255))
        img_cv2 = numpy.asarray(img_pil)
        img = cv2.cvtColor(img_cv2, cv2.COLOR_RGB2BGR)
        cv2.imshow('video', img)
    if cv2.waitKey(1) & 0xFF == 27:
        break
capture.release()



# import cv2
# from PIL import Image, ImageDraw
# import numpy
#
#
# capture = cv2.VideoCapture(0)
#
# while True:
#     ret, frame = capture.read()
#     if ret:
#         img_pil = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
#         draw_img = ImageDraw.Draw(img_pil)
#         draw_img.text((100, 100), 'test', fill=(0, 255, 255))
#         img_cv2 = numpy.asarray(img_pil)
#         img = cv2.cvtColor(img_cv2, cv2.COLOR_RGB2BGR)
#         cv2.imshow('video', img)
#     if cv2.waitKey(1) & 0xFF == 27:
#         break
#
# capture.release()

