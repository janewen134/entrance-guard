import face_recognition
import cv2
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import datetime
import threading
import time
import yagmail

# mail = yagmail.SMTP(user='3345317820@qq.com', password='okljmkovxxetcjdg', host='smtp.qq.com')
# mail.send('3345317820@qq.com', 'yagmailTest', 'this is a test mail.')


class Recorder:
    pass


record_dic = {}
unknownjpg = []


def sendmail(title, contents, fileslist):
    yag = yagmail.SMTP(user='3345317820@qq.com', password='okljmkovxxetcjdg', host='smtp.qq.com')
    yag.send('3345317820@qq.com', title, contents, fileslist)


def dicttostr():
    strlist = []
    listkey = list(sorted(record_dic.keys()))
    for item in listkey:
        strlist.extend([item + ',' + str(onetime) for onetime in record_dic[item].times])
    return strlist


flagover = 0


def saveRecorder(name, frame):
    global record_dic
    global flagover
    global unknownjpg
    if flagover == 1:
        return
    try:
        red = record_dic[name]
        # rec.times[-1]获取最后一次记录的时间
        secondsDiff = (datetime.datetime.now()-red.times[-1]).total_seconds()

        if secondsDiff < 60*10:
            return
        red.times.append(datetime.datetime.now())
        print('更新记录', record_dic, red.times)
    except (KeyError):
        newRed = Recorder()
        newRed.times = [datetime.datetime.now()]
        record_dic[name] = newRed
        print('添加记录', record_dic, newRed.times)

    if name == '未知头像':
        # 这个s是最后一次记录的时间
        s = str(record_dic[name].times[-1])
        print('写入', s[:10]+s[-6:])
        filename = s[:10]+s[-6:]+'.jpg'
        cv2.imwrite('./temp/' + filename, frame)
        unknownjpg.append('./temp/'+filename)


def loop_timer_headle():
    print('-------Timer headle!-----------', str(datetime.datetime.now()))
    global timer2
    global flagover
    global record_dic
    global unknownjpg
    flagover = 1
    timer2 = threading.Timer(60*1, loop_timer_headle)
    timer2.start()

    # 如果mail_content不为空，则发送邮件通知
    mail_content = '\n'.join(dicttostr())
    if mail_content.strip():
        sendmail('来访统计记录', mail_content, unknownjpg)
        print('来访登记记录邮件已经发送', mail_content)

    record_dic.clear()
    unknownjpg.clear()
    print('清空')

    time.sleep(10)
    print('重新开始')
    flagover = 0


timer2 = threading.Timer(2, loop_timer_headle)
timer2.start()


def load_img(sample_dir):
    print('loading sample face..')

    for (dirpath, dirnames, filenames) in os.walk(sample_dir):
        print(dirpath, dirnames, filenames)
        facelib = []
        for filename in filenames:
            filename_path = os.sep.join([dirpath, filename])
            faceimage = face_recognition.load_image_file(filename_path)
            face_encoding = face_recognition.face_encodings(faceimage)[0]
            facelib.append(face_encoding)
        return facelib, filenames


facelib, facename = load_img('./facelib')
video_capture = cv2.VideoCapture(0)

face_locations = []
face_encodings = []
process_this_frame = True

while True:
    ret, frame = video_capture.read()
    '''
    resize方法用于绽放图像，第一个参数是待绽放的图像，第二个参数指绽放尺寸大小dsize.
    如果指定dsize为（０，０），则表示按后面的ｆｘ和ｆｙ作为绽放比例。
    ｄｓｉｚｅ和ｆｘ／ｆｙ不能同时为０。
    '''
    # 将图像缩小1/4，为人脸识别提速
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    # opencv的图像格式默认为BGR格式，大家可以想象成像素排列跟RGB格式不一样，所以我们必须做一点调整
    # 将像素点进行反向，将opencv的BGR格式转为RGB格式
    rgb_small_frame = small_frame[:, :, ::-1]

    # 找到人的位置并生成特征码
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    # print('人脸特征编码长度’， len(face_encodings))

    face_names = []  # 定义列表旋转识别结果
    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(facelib, face_encoding, tolerance=0.39)  # 人脸识别，阈值为经验值
        name = '未知头像' #定义默认的识别结果为unknow
        # print('匹配结果：’， matches)
        if True in matches:  # 如果识别出来，就将名称取出
            first_match_index = matches.index(True)
            name = facename[first_match_index][:-4]
        face_names.append(name)  # 保存识别结果

    # 显示结果
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)  # 标注人脸

        img_PIL = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))  #转换图片格式
        font = ImageFont.truetype('simhei.ttf', 40)   # 加载字体
        position = (left+6, bottom-6)                 # 指定文字位置
        draw = ImageDraw.Draw(img_PIL)                # 绘制图片
        draw.text(position, name, font=font, fill=(0, 0, 255))  # 绘制文字
        frame = cv2.cvtColor(np.asarray(img_PIL), cv2.COLOR_RGB2BGR)   # 将图片颜色转回OpenCV格式
        saveRecorder(name, frame)
    cv2.imshow('video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()    # 释放摄像头资源
# cv2.destroyAllWindows()
time.sleep(2)
timer2.cancel()

















