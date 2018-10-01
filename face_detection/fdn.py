# coding:utf-8

import cv2


def Get_Face_Num(imgPath):

    # 加载图片
    img = cv2.imread(imgPath)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 人脸识别的训练数据
    face_cascade = cv2.CascadeClassifier(r'./model.xml')
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=3,
        minNeighbors=5,
        minSize=(5, 5),
    )
    print("{0}发现{1}张人脸!".format(imgPath, len(faces)))
    return len(faces)


if __name__ == "__main__":
    while True:
        path = input("path:")
        if path == "q" or path == "Q":
            break
        else:
            Get_Face_Num(path)
