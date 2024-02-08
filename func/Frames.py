import configparser
import json
import os
import random
import time
from datetime import datetime
from pprint import pprint
import cv2
import numpy as np
from func.Rectang import Rectang
# from keras import models
from func.about_image import putTextRect, putTextRectlist
import sys
from func.TextColor import *
from func.ini_file import ini_to_dict, dict_to_ini
import pygame


def to_xydxdy(x1, y1, w, h, shape):
    x = (x1 + w / 2) / shape[0]
    y = (y1 + h / 2) / shape[1]
    dx = w / shape[0]
    dy = h / shape[1]
    return x, y, dx, dy




class Frame:
    def __init__(self, name: str, rectang: Rectang, model_used: str, pcb_frame_name=None):
        self.name = name
        if pcb_frame_name:
            self.pcb_frame_name = pcb_frame_name
        else:
            self.pcb_frame_name = name
        self.rect = rectang
        self.model_used = model_used
        self.res_show = None
        self.img = None
        self.debug_res_name = '-'
        self.reset_result()

    def __str__(self):
        return (f'{PINK}Frame {GREEN}{self.name}{ENDC} ({self.rect.__str__()})')

    def reset_result(self):
        self.predictions_score_list = None  # [ -6.520611   8.118368 -21.86103   22.21528 ]
        self.percent_score_list = None  # [3.3125e-11 7.5472e-05 7.2094e-18 9.9999e+01]
        self.highest_score_number = None  # ตำแหน่งไหน # 3
        self.highest_score_percent = None
        self.highest_score_name = None


class Model:
    def __init__(self, name, status_list):
        self.name = name
        self.status_list = status_list
        self.model = None

    def __str__(self):
        return (f'{BLUE}Model {GREEN}{self.name}{ENDC}')

    def load_model(self, modelname):
        try:
            self.model = models.load_model(fr'data/{modelname}/model/{self.name}.h5')
        except Exception as e:
            print(f'{YELLOW}function "load_model" error.\n'
                  f'file error data/{modelname}/model/{self.name}.h5{ENDC}\n'
                  f'{str(e)}')
            # sys.exit()

        try:
            status_list = json.loads(open(fr'data/{modelname}/model/{self.name}.json').read())
            if status_list != self.status_list:
                print(f'{YELLOW}status_list model != self.status_list')
                print(f'status_list from model = {status_list}')
                print(f'self.status_list       = {self.status_list}{ENDC}')
        except Exception as e:
            print(f'{YELLOW}function "load_model" error.\n'
                  f'file error data/{modelname}/model/{self.name}.json{ENDC}'
                  f'{str(e)}')
            # sys.exit()


class Mark:
    def __init__(self, name, rect: Rectang, k):
        self.name = name
        self.rect = rect
        self.k = k

    def __str__(self):
        return (f'{CYAN}Mark {GREEN}{self.name}{ENDC}')


class Frames:
    def __init__(self, path: os.path):
        self.path = path
        self.frames_path = os.path.join(self.path, 'ini_frames.ini')
        self.models_path = os.path.join(self.path, 'ini_models.ini')
        self.marks_path = os.path.join(self.path, 'ini_marks.ini')
        self.name = os.path.basename(self.path)
        self.frames = {}
        self.models = {}
        self.marks = {}

        frames = ini_to_dict(self.frames_path, )
        models = ini_to_dict(self.models_path, )
        marks = ini_to_dict(self.marks_path, )
        pprint(marks)
        for k, v in frames.items():
            self.frames[k] = Frame(k, Rectang(*v['xydxdy']), v['model_used'])
        for k, v in models.items():
            self.models[k] = Model(k, v['status_list'])
        for k, v in marks.items():
            self.marks[k] = Mark(k, Rectang(*v['xydxdy']), Rectang(*v['area_xydxdy']))

        for k, v in self.frames.items():
            print(k, v)
        for k, v in self.models.items():
            print(k, v)
        for k, v in self.marks.items():
            print(k, v)

    def __str__(self):
        return f'{PINK}{BOLD}        ╔ {ENDC}{len(self.frames)} frame is {GREEN}{", ".join(self.frames.keys())}{ENDC}\n' \
               f'{PINK}{BOLD} Frames ╣ {ENDC}{len(self.models)} model is {GREEN}{", ".join(self.models.keys())}{ENDC}\n' \
               f'{PINK}{BOLD}        ╚ {ENDC}{len(self.marks)}  mark  is {GREEN}{", ".join(self.marks.keys())}{ENDC}\n'

    def save_mark(self, img):
        h, w, _ = img.shape
        for name, mark in self.marks.items():
            x1, y1, x2, y2, = mark.rect.to_pix_xyxy()
            print(f'{GREEN}save "data/{self.name}/{name}.png"{ENDC}')
            cv2.imwrite(f'data/{self.name}/{name}.png', img[y1:y2, x1:x2])


if __name__ == '__main__':
    frames = Frames(os.path.join("..", "data", 'D07 QM7-3238'))
    print(frames)

# img = np.full((1080, 1920, 3), (10, 10, 10), np.uint8)
# frames = Frames(json.loads(open(r"data\D07\frames pos.json").read()))
# frames.add_mark(json.loads(open(rf"data\D07\mark pos.json").read()))
# print(frames)
# print(frames.frames[0])
# print(frames.frames[0].x)
#
# frames.draw_frame(img)
# cv2.imshow('img', img)
# cv2.waitKey(0)
