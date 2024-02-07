import json
import random
import time
from datetime import datetime
import cv2
import numpy as np
from keras import models
from func.about_image import putTextRect, putTextRectlist
import sys
from func.TextColor import *

class Dtime():
    def __init__(self):
        self.t1 = {}  # {t1:datetime}
        self.s_list = {}  # {t1:[]}

    def start(self, t):
        self.t1[t] = datetime.now()

    def stop(self, t):
        t2 = datetime.now()
        dt_seconds = (t2 - self.t1[t]).total_seconds()
        if t not in self.s_list.keys():
            self.s_list[t] = []
        self.s_list[t].append(dt_seconds)

    def reset(self):
        for i in range(len(self.s_list)):
            self.s_list[i] = []

    def show(self):
        try:
            for t, v in self.s_list.items():
                dtime = self.s_list[t][-1]
                lenlist = len(self.s_list[t])
                mean = f'{sum(self.s_list[t]) / lenlist:.3f}'
                tmin = f'{min(self.s_list[t]):.3f}'
                tmax = f'{max(self.s_list[t]):.3f}'

                print(f'{dtime:.3f}s / min = {tmin}s / max = {tmax}s / mean = {mean}s  <--{t} {lenlist}')
            print()
        except:
            pass


def drawline(img, pt1, pt2, color, thickness=1, gap=10):
    dist = ((pt1[0] - pt2[0]) ** 2 + (pt1[1] - pt2[1]) ** 2) ** .5
    pts = []
    for i in np.arange(0, dist, gap):
        r = i / dist
        x = int((pt1[0] * (1 - r) + pt2[0] * r) + .5)
        y = int((pt1[1] * (1 - r) + pt2[1] * r) + .5)
        p = (x, y)
        pts.append(p)

    e = pts[0]
    i = 0
    for p in pts:
        s = e
        e = p
        if i % 2 == 1:
            cv2.line(img, s, e, color, thickness)
        i += 1


def drawpoly(img, pts, color, thickness=1):
    for i in range(len(pts)):
        s = pts[i - 1]
        e = pts[i]
        drawline(img, s, e, color, thickness)


def drawrect(img, pt1, pt2, color, thickness=1):
    pts = [pt1, (pt2[0], pt1[1]), pt2, (pt1[0], pt2[1])]
    drawpoly(img, pts, color, thickness)


class Frame:
    def __init__(self, name, x, y, dx, dy, model_used, res_show, pcb_frame_name=None):
        self.name = name
        if pcb_frame_name:
            self.pcb_frame_name = pcb_frame_name
        else:
            self.pcb_frame_name = name
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.model_used = model_used
        self.res_show = res_show
        self.x1 = x - dx / 2
        self.y1 = y - dy / 2
        self.x2 = x + dx / 2
        self.y2 = y + dy / 2
        self.img = None
        self.debug_res_name = '-'
        self.reset_result()
        self.K_color = {
            'ok': (0, 255, 0),
            'nopart': (0, 0, 255),
            'wrongpart': (0, 150, 255),
            'wrongpolarity': (150, 0, 255)
        }

    def __str__(self):
        return (f'{PINK}Frame '
                f'{GREEN}{self.name}{ENDC}')

    def reset_result(self):
        self.color_frame = (0, 255, 255)
        self.color_frame_thickness = 5
        self.color_text = (255, 255, 255)
        self.font_size = 2.5
        self.predictions_score_list = None  # [ -6.520611   8.118368 -21.86103   22.21528 ]
        self.percent_score_list = None  # [3.3125e-11 7.5472e-05 7.2094e-18 9.9999e+01]
        self.highest_score_number = None  # ตำแหน่งไหน # 3
        self.highest_score_percent = None
        self.highest_score_name = None

    def resShow(self):
        for key, values in self.res_show.items():
            if self.highest_score_name in values:
                return key
        return self.highest_score_name


class Model:
    def __init__(self, name, status_list):
        self.name = name
        self.status_list = status_list
        self.model = None

    def __str__(self):
        return (f'{BLUE}Model '
                f'{GREEN}{self.name}{ENDC}')

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
    def __init__(self, name, x, y, dx, dy, k):
        self.name = name
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.k = k

        self.x1 = x - dx / 2
        self.y1 = y - dy / 2
        self.x2 = x + dx / 2
        self.y2 = y + dy / 2

    def __str__(self):
        return (f'{CYAN}Mark '
                f'{GREEN}{self.name}{ENDC}')

    def rec_around(self, h, w):
        x1px = int(self.x1 * w)
        y1px = int(self.y1 * h)
        x2px = int(self.x2 * w)
        y2px = int(self.y2 * h)
        kx = int((x2px - x1px) * self.k)
        ky = int((y2px - y1px) * self.k)
        return (x1px - kx, y1px - ky), (x2px + kx, y2px + ky)

    def rec_mark(self, h, w):
        x1px = int(self.x1 * w)
        y1px = int(self.y1 * h)
        x2px = int(self.x2 * w)
        y2px = int(self.y2 * h)
        return (x1px, y1px), (x2px, y2px)

    def xpx(self, h, w):
        return int(self.x * w)

    def ypx(self, h, w):
        return int(self.y * h)

    def xypx(self, h, w):
        return self.xpx(h, w), self.ypx(h, w)


class Frames:
    def __init__(self, path):
        data_all = json.loads(open(path).read())
        self.frames = {}
        self.models = {}
        self.marks = {}

        for name, v in data_all['frames'].items():
            x = v['x']
            y = v['y']
            dx = v['dx']
            dy = v['dy']
            model_used = v['model_used']
            res_show = v['res_show']
            pcb_frame_name = v.get('pcb_frame_name')
            self.frames[name] = Frame(name, x, y, dx, dy, model_used, res_show, pcb_frame_name)
        for name, v in data_all['models'].items():
            status_list = sorted(v['status_list'])
            self.models[name] = Model(name, status_list)
        if data_all.get('marks'):
            for name, v in data_all['marks'].items():
                x = v['x']
                y = v['y']
                dx = v['dx']
                dy = v['dy']
                k = v['k']
                self.marks[name] = Mark(name, x, y, dx, dy, k)

        self.len = len(self.frames)
        self.color_frame = (255, 255, 255)

    def __str__(self):
        return f'{PINK}{BOLD}        ╔ {ENDC}{len(self.frames)} frame is {GREEN}{", ".join(self.frames.keys())}{ENDC}\n' \
               f'{PINK}{BOLD} Frames ╣ {ENDC}{len(self.models)} model is {GREEN}{", ".join(self.models.keys())}{ENDC}\n' \
               f'{PINK}{BOLD}        ╚ {ENDC}{len(self.marks)}  mark  is {GREEN}{", ".join(self.marks.keys())}{ENDC}\n'


    def save_mark(self, img):
        h, w, _ = img.shape
        for name, mark in self.marks.items():
            x = mark.x
            y = mark.y
            dx = mark.dx
            dy = mark.dy
            x1 = int((x - dx / 2) * w)
            y1 = int((y - dy / 2) * h)
            x2 = int((x + dx / 2) * w)
            y2 = int((y + dy / 2) * h)
            print(f'{GREEN}save "data/{self.name}/{name}.png"{ENDC}')
            cv2.imwrite(f'data/{self.name}/{name}.png', img[y1:y2, x1:x2])
            cv2.imshow('img', img[y1:y2, x1:x2])



if __name__ == '__main__':
    framesmodel = Frames(rf"..\data\{'D07 QM7-3238'}\frames pos.json")
    print(framesmodel)
    # print(frame.model_used)

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
