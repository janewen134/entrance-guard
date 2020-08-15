import dlib
import cv2


detector = dlib.get_frontal_face_detector()   #获得一个脸部检测器，其包含了脸部检测的算法
win = dlib.image_window()
img = cv2.imread('./imgs/me.jpg')
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
result = detector(img, 1)  # 第2个参数 1 表示的是图像像素被放大1倍，以便获得得图像更多的细节
win.set_image(img)
win.add_overlay(result)
dlib.hit_enter_to_continue()


