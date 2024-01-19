import json
import os
import time
from datetime import datetime
import cv2
import numpy as np
import pygame
from func.about_image import putTextRect, overlay
import requests
from Frames import BLACK, FAIL, GREEN, WARNING, BLUE, PINK, CYAN, ENDC, BOLD, ITALICIZED, UNDERLINE

def mkdir(directory):
    if not os.path.exists(directory):
        os.mkdir(directory)
def remove(directory):
    if os.path.exists(directory):
      os.remove(directory)

####################################################################################
mouse_event = False
mouse_pos = 0, 0



class Exit:
    def __init__(self, img_BG=None):
        if img_BG is not None:
            self.img_BG = img_BG//4
            # self.img_BG = cv2.blur(img_BG, (5, 5))
        else:
            self.img_BG = np.zeros((1080, 1920, 3), np.uint8)
        self.x_shift = 0
        self.y_shift = 0
        self.img = cv2.imread('ui/windows_Exit/non.png')
        self.img_ac = cv2.imread('ui/windows_Exit/ac.png')
        pos = json.loads(open('ui/windows_Exit/pos.json').read())
        self.buttons = {}
        for k, v in pos.items():
            x1pix, y1pix, x2pix, y2pix = v
            self.buttons[k] = Button(k, x1pix=x1pix, y1pix=y1pix, x2pix=x2pix, y2pix=y2pix)

    def update(self, mouse_pos, events):
        x, y = mouse_pos
        x -= self.x_shift
        y -= self.y_shift

        self.img_show = self.img.copy()
        for k, v in self.buttons.items():
            # v.show_frame_for_debug(self.img_show)
            self.img_show = v.show_button_ac(self.img_show, self.img_ac, (x, y))

        for k, v in self.buttons.items():
            res = None
            # if mouse_event:
            #     print(pygame.MOUSEBUTTONUP,mouse_event)
            for event in events:
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    if v.mouse_on_button(x, y):
                        res = k
                        return res

        self.img_BG = overlay(self.img_BG, self.img_show, (self.x_shift, self.y_shift))
        return res


class TextInput:
    def __init__(self, img_BG=None):
        if img_BG is not None:
            self.img_BG = img_BG // 4
            # self.img_BG = cv2.blur(img_BG, (5, 5))
        else:
            self.img_BG = np.zeros((1080, 1920, 3), np.uint8)
        self.x_shift = 0
        self.y_shift = 0
        self.img = cv2.imread('ui/windows_Text/non.png')
        self.img_ac = cv2.imread('ui/windows_Text/ac.png')
        pos = json.loads(open('ui/windows_Text/pos.json').read())
        self.buttons = {}
        for k, v in pos.items():
            x1pix, y1pix, x2pix, y2pix = v
            self.buttons[k] = Button(k, x1pix=x1pix, y1pix=y1pix, x2pix=x2pix, y2pix=y2pix)
        self.textinput = ''

    def update(self, mouse_pos, events):
        x, y = mouse_pos
        x -= self.x_shift
        y -= self.y_shift

        self.img_show = self.img.copy()
        cv2.putText(self.img_show, self.textinput, (40, 73), 16, 0.45, (255, 255, 255), 1, cv2.LINE_AA)
        for k, v in self.buttons.items():
            # v.show_frame_for_debug(self.img_show)
            self.img_show = v.show_button_ac(self.img_show, self.img_ac, (x, y))

        for k, v in self.buttons.items():
            res = None
            print('---')
            for event in events:
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    if v.mouse_on_button(x, y):
                        res = k
                        return res
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        self.textinput = self.textinput[:-1]
                    elif event.unicode in ('abcdefghijklmnopqrstuvwxyz 0123456789+-_=()[]{}'
                                           'ABCDEFGHIJKLMNOPQRSTUVWXYZ `~!@#$%^&;.'
                                           ):
                        self.textinput += event.unicode

        self.img_BG = overlay(self.img_BG, self.img_show, (self.x_shift, self.y_shift))
        return res


class Setting:
    def __init__(self, img_BG=None):
        if img_BG is not None:
            self.img_BG = img_BG // 4
            # self.img_BG = cv2.blur(img_BG, (20, 20))
        else:
            self.img_BG = np.zeros((1080, 1920, 3), np.uint8)
        self.x_shift = 0
        self.y_shift = 0
        self.img = cv2.imread('ui/windows_Setting/non.png')
        self.img_ac = cv2.imread('ui/windows_Setting/ac.png')
        pos = json.loads(open('ui/windows_Setting/pos.json').read())
        self.buttons = {}
        for k, v in pos.items():
            x1pix, y1pix, x2pix, y2pix = v
            self.buttons[k] = Button(k, x1pix=x1pix, y1pix=y1pix, x2pix=x2pix, y2pix=y2pix)
        self.read_check_box_data()
        self.ipIO = 'http://192.168.225.198:8080'
        self.ipIO = 'http://192.168.225.198:8080'

    def read_check_box_data(self):
        try:
            self.check_box = json.loads(open('ui/windows_Setting/check box.json').read())
        except:
            self.check_box = {
                'Show name': True,
                'Show results from predictions': True,
                'Show %results from predictions': True,
                'Show list class name': False,

                'Change color frame': True,
                'Change color name': False,
                'Change color results from predictions': False,
                'Change color %results from predictions': False,
                'Change color list class name': False,
            }

    def update(self, mouse_pos, events):
        x, y = mouse_pos
        x -= self.x_shift
        y -= self.y_shift

        self.img_show = self.img.copy()

        # data_dict = self.readIO()
        # if type(data_dict) == dict:
        #     line = -1
        #     for k, v in data_dict.items():
        #         line += 1
        #         cv2.putText(self.img_show, f'{v} = {k}',
        #                     (40, 300 + line * 20), 16, 0.45, (255, 255, 255), 1, cv2.LINE_AA)

        # else:
        #     cv2.putText(self.img_show, f'error',
        #                 (40, 300), 16, 0.45, (255, 255, 255), 1, cv2.LINE_AA)

        for k, v in self.buttons.items():
            # v.show_frame_for_debug(self.img_show)
            if k in self.check_box.keys() and self.check_box[k]:
                self.img_show = v.change_status_img(self.img_show, self.img_ac[:, 18:])  # ถ้าจริงให้ติกถูก
                self.img_show = v.show_button_ac(self.img_show, self.img_ac[:, 36:], (x, y))
            else:
                self.img_show = v.show_button_ac(self.img_show, self.img_ac, (x, y))

        for k, v in self.buttons.items():
            res = None
            for event in events:
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    if v.mouse_on_button(x, y):
                        res = k
                        if res in self.check_box.keys():
                            if self.check_box[k]:
                                self.check_box[k] = False
                            else:
                                self.check_box[k] = True
                        if res in ['Button_LED_1 ON', 'Button_LED_1 OFF',
                                   'Button_LED_2 ON', 'Button_LED_2 OFF',
                                   'Stopper_1 ON', 'Stopper_1 OFF',
                                   'Stopper_2 ON', 'Stopper_2 OFF']:
                            pin = res.split(' ')[0]
                            out = res.split(' ')[1].lower()
                            self.writeIO(pin, out)

                        return res
        self.img_BG = overlay(self.img_BG, self.img_show, (self.x_shift, self.y_shift))
        return res

    def readIO(self):
        res = requests.get(f'{self.ipIO}/readpinall')
        if res.status_code == 200:
            data_dict = json.loads(res.text)
            return data_dict

    def writeIO(self, pin, status):
        print(f'{self.ipIO}/{status}/{pin}')
        requests.get(f'{self.ipIO}/{status}/{pin}')


class Wait:
    def __init__(self, img_BG=None):
        if img_BG is not None:
            self.img_BG = img_BG // 4
            # self.img_BG = cv2.blur(img_BG, (5, 5))
        else:
            self.img_BG = np.zeros((1080, 1920, 3), np.uint8)
        self.x_shift = 0
        self.y_shift = 0
        self.img = cv2.imread('ui/windows_wait/non.png')
        self.img_ac = cv2.imread('ui/windows_wait/ac.png')
        pos = json.loads(open('ui/windows_wait/pos.json').read())
        self.buttons = {}
        for k, v in pos.items():
            x1pix, y1pix, x2pix, y2pix = v
            self.buttons[k] = Button(k, x1pix=x1pix, y1pix=y1pix, x2pix=x2pix, y2pix=y2pix)
        self.time = datetime.now()

    def set_val(self, sub, *args):
        cv2.putText(self.img, sub, (68, 35), 2, 0.59, (255, 255, 255), 1, cv2.LINE_AA)
        line = 0
        for txt in args:
            cv2.putText(self.img, txt, (68, int(63 + 20 * line)), 16, 0.45, (255, 255, 255), 1, cv2.LINE_AA)
            line += 1

    def update(self, mouse_pos, events, count_time=True):
        x, y = mouse_pos
        x -= self.x_shift
        y -= self.y_shift

        self.img_show = self.img.copy()
        if count_time:
            cv2.putText(self.img_show, f'{(datetime.now() - self.time).total_seconds():.1f}s',
                        (68, 63), 16, 0.45, (255, 255, 255), 1, cv2.LINE_AA)

        for k, v in self.buttons.items():
            # v.show_frame_for_debug(self.img_show)
            self.img_show = v.show_button_ac(self.img_show, self.img_ac, (x, y))
        for k, v in self.buttons.items():
            res = None
            for event in events:
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    if v.mouse_on_button(x, y):
                        res = k
                        return res
        self.img_BG = overlay(self.img_BG, self.img_show, (self.x_shift, self.y_shift))
        return res


class Confirm:
    def __init__(self, img_BG=None):
        if img_BG is not None:
            self.img_BG = img_BG // 4
            # self.img_BG = cv2.blur(img_BG, (5, 5))
        else:
            self.img_BG = np.zeros((1080, 1920, 3), np.uint8)
        self.x_shift = 0
        self.y_shift = 0
        self.img = cv2.imread('ui/windows_Confirm/non.png')
        self.img_ac = cv2.imread('ui/windows_Confirm/ac.png')
        pos = json.loads(open('ui/windows_Confirm/pos.json').read())
        self.buttons = {}
        for k, v in pos.items():
            x1pix, y1pix, x2pix, y2pix = v
            self.buttons[k] = Button(k, x1pix=x1pix, y1pix=y1pix, x2pix=x2pix, y2pix=y2pix)

    def set_val(self, sub, *args):
        cv2.putText(self.img, sub, (68, 35), 2, 0.59, (255, 255, 255), 1, cv2.LINE_AA)
        line = 0
        for txt in args:
            cv2.putText(self.img, txt, (68, int(63 + 20 * line)), 16, 0.45, (255, 255, 255), 1, cv2.LINE_AA)
            line += 1

    def update(self, mouse_pos, events):
        x, y = mouse_pos
        x -= self.x_shift
        y -= self.y_shift
        self.img_show = self.img.copy()
        for k, v in self.buttons.items():
            # v.show_frame_for_debug(self.img_show)
            self.img_show = v.show_button_ac(self.img_show, self.img_ac, (x, y))
        for k, v in self.buttons.items():
            res = None
            for event in events:
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    if v.mouse_on_button(x, y):
                        res = k
                        return res
        self.img_BG = overlay(self.img_BG, self.img_show, (self.x_shift, self.y_shift))
        return res


class Select:
    def __init__(self, img_BG=None):
        if img_BG is not None:
            self.img_BG_ori = img_BG
        else:
            self.img_BG_ori = np.zeros((1080, 1920, 3), np.uint8)

        self.x_shift = 0
        self.y_shift = 0
        self.img = cv2.imread('ui/select/non.png')
        self.img_ac = cv2.imread('ui/select/ac.png')
        self.pos = json.loads(open('ui/select/pos.json').read())

        x1pix, y1pix, x2pix, y2pix = self.pos['top']
        self.top_img = self.img[y1pix:y2pix, x1pix:x2pix]
        x1pix, y1pix, x2pix, y2pix = self.pos['data']
        self.data_img = self.img[y1pix:y2pix, x1pix:x2pix]
        self.data_img_ac = self.img_ac[y1pix:y2pix, x1pix:x2pix]
        x1pix, y1pix, x2pix, y2pix = self.pos['bottom']
        self.bottom_img = self.img[y1pix:y2pix, x1pix:x2pix]
        self.data_all = []
        self.data_show = []
        self.page = 0
        self.buttons = {}
        self.n_max_data = 30

    def n_data(self, page):
        if len(self.data_all) <= self.n_max_data:
            self.data_show = self.data_all
            return 0
        else:
            self.data_show = self.data_all[30 * page:30 * (page + 1)] + ['- next -']
            return len(self.data_all) % self.n_max_data


    def add_data(self, *args):
        for i in args:
            self.data_all.append(i)
        self.setup_data()

    def next_page(self):
        self.page += 1
        if self.page * self.n_max_data > len(self.data_all):
            self.page = 0
        self.setup_data()

    def setup_data(self):
        self.n_data(self.page)
        n = len(self.data_show)
        self.img = np.concatenate((self.top_img, *(self.data_img,) * n, self.bottom_img), axis=0)
        self.img_ac = np.concatenate((self.top_img, *(self.data_img_ac,) * n, self.bottom_img), axis=0)
        for i in range(n):
            name = self.data_show[i]
            x1pixt, y1pixt, x2pixt, y2pixt = self.pos['top']  # [0, 0, 325, 8]
            x1pixd, y1pixd, x2pixd, y2pixd = self.pos['data']  # [0, 9, 325, 33]
            x1 = x1pixt
            x2 = x2pixt
            y1 = y2pixt + (y2pixd - y1pixd) * i
            y2 = y2pixt + (y2pixd - y1pixd) * (i + 1)
            self.buttons[f'{name}'] = Button(f'{name}', x1pix=x1, y1pix=y1, x2pix=x2, y2pix=y2)
            cv2.putText(self.img, f'{name}', (20, y1 + 17), 16, 0.45, (255, 255, 255), 1, cv2.LINE_AA)
            cv2.putText(self.img_ac, f'{name}', (20, y1 + 17), 16, 0.45, (100, 255, 100), 2, cv2.LINE_AA)

    def update(self, mouse_pos, events):
        x, y = mouse_pos
        x -= self.x_shift
        y -= self.y_shift

        self.img_show = self.img.copy()
        for k, v in self.buttons.items():
            # v.show_frame_for_debug(self.img_show)
            self.img_show = v.show_button_ac(self.img_show, self.img_ac, (x, y))

        res = None
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                res = 'break, Click the mouse on an empty space.'
                for k, v in self.buttons.items():
                    if v.mouse_on_button(x, y):
                        res = k
            if event.type == pygame.MOUSEBUTTONUP and event.button == 3:
                res = 'break, Click R mouse'
        self.img_BG = overlay(self.img_BG_ori, self.img_show, (self.x_shift, self.y_shift))
        if res:
            print(f'{ITALICIZED}Select click --> {UNDERLINE}{res}{ENDC}')
        return res


class Display:
    def __init__(self):
        self.x_shift = 0
        self.y_shift = 0
        self.img = cv2.imread('ui/display/non.png')
        self.img_ac = cv2.imread('ui/display/ac.png')
        pos = json.loads(open('ui/display/pos.json').read())
        self.buttons = {}
        for k, v in pos.items():
            x1pix, y1pix, x2pix, y2pix = v
            self.buttons[k] = Button(k, x1pix=x1pix, y1pix=y1pix, x2pix=x2pix, y2pix=y2pix)
        self.LOW = 0
        self.HIGH = 1
        self.ipIO = 'http://192.168.225.198:8080'
        self.mode = 'run'  # debug, manual, run
        self.mode_run_step = 0
        self.update_dis_res = set()
        self.predict_time = None
        self.predict_res = None
        self.old_res = None
        self.select_model = None

    def update(self, mouse_pos, events):
        x, y = mouse_pos
        x -= self.x_shift
        y -= self.y_shift

        self.img_show = self.img.copy()
        for k, v in self.buttons.items():
            # v.show_frame_for_debug(self.img_show)
            if 'mode_menu' in k and self.mode == k.split('-')[1]:
                self.img_show = v.change_status_img(self.img_show, self.img_ac[:, 40:])
            else:
                self.img_show = v.show_button_ac(self.img_show, self.img_ac, (x, y))

        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                for k, v in self.buttons.items():
                    if v.mouse_on_button(x, y):
                        if event.button == 1 or event.button == 3:
                            res = k
                            if event.button == 3:
                                res = f'm3:{k}'
                            if 'mode_menu' in res:
                                self.mode = res.split('-')[1]
                            if res == 'predict':
                                self.update_dis_res.add('adj image')
                            self.update_dis_res.add(res)
                            print(f'{GREEN}{ITALICIZED}display click --> {UNDERLINE}{res}{ENDC}')
        return self.img_show
