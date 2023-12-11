import cv2
import os

def conver_vid_to_img(vid_path, img_path):
    os.makedirs(img_path, exist_ok=True)
    vidcap = cv2.VideoCapture(vid_path)
    success, image = vidcap.read()
    count = 0
    while success:
        cv2.imwrite(img_path + "frame%d.jpg" % count, image)  # save frame as JPEG file
        success, image = vidcap.read()
        print("Read a new frame: ", success)
        count += 1

def convert_all():
    for i in range(0, 4):
        conver_vid_to_img("data/" + str(i) + ".MOV", "data/img/" + str(i) + "/")


convert_all()
