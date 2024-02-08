def capture(data):
    import cv2
    import time

    def reset():
        cap = cv2.VideoCapture(0)
        cap.set(3, 3264)
        cap.set(4, 2448)
        return cap

    cap = reset()
    while data['is_running']:
        if data['reconnect_cam']:
            data['reconnect_cam'] = False
            data['capture res'] = (False, None)
            cap = reset()

        if data['capture']:
            if data['capture'] == 1:
                data['capture'] = 0
            data['capture res'] = cap.read()
            # cv2.imshow('img', data['capture res'][1])
            # cv2.waitKey(1)
        else:
            time.sleep(0.5)


def req_io_box(data):
    import requests
    import time
    from func.TextColor import *
    time.sleep(5)

    while not stop_event.is_set():
        read = data['read data']
        try:
            res = requests.get(read['url'], timeout=0.5)
            read['status code'] = res.status_code
            read['res_text'] = res.text
        except requests.exceptions.Timeout:
            read['status code'] = 0
            read['res_text'] = 'Timeout. The request took longer than 0.5 second to complete.'
        except requests.exceptions.RequestException as e:
            read['status code'] = 0
            read['res_text'] = f'{e}'
        data['read data'] = read
        time.sleep(0.8)

        write = data['write data']
        if write['input data'] != write['res_text'].split('write>')[-1] or write['status code'] != 200:
            try:
                res = requests.get(write['url'].replace('<data>', write['input data']), timeout=0.5)
                write['status code'] = res.status_code
                write['res_text'] = res.text
            except requests.exceptions.Timeout:
                write['status code'] = 0
                write['res_text'] = 'Timeout. The request took longer than 0.5 second to complete.'
            except requests.exceptions.RequestException as e:
                write['status code'] = 0
                write['res_text'] = f'{e}'
            data['write data'] = write
        time.sleep(0.8)


def printdata(data):
    import time
    from pprint import pprint
    from func.TextColor import *
    while data['is_running']:
        print(PINK, UNDERLINE)
        pprint(data['requests']['read data'])
        pprint(data['requests']['write data'])
        print(ENDC)
        time.sleep(1)


if __name__ == '__main__':
    import cv2
    import numpy as np
    import multiprocessing
    import json
    import os
    from main import main

    stop_event = multiprocessing.Event()
    manager = multiprocessing.Manager()
    data = manager.dict()
    data['capture'] = 0,  # 0=don't cap, 1=one time, 2=all time
    data['capture res'] = (False, None)
    data['reconnect_cam'] = False
    data['is_running'] = True
    data['mode'] = 'debug'  # debug, manual, auto
    data['tool'] = 'select'  # select,set frame

    capture_process = multiprocessing.Process(target=capture, args=(data,))
    show_process = multiprocessing.Process(target=main, args=(data,))
    # req_io_box_process = multiprocessing.Process(target=req_io_box, args=(data,))
    # printdata_process = multiprocessing.Process(target=printdata, args=(data, stop_event))

    capture_process.start()
    show_process.start()
    # req_io_box_process.start()
    # printdata_process.start()

    capture_process.join()
    show_process.join()
    # req_io_box_process.join()
    # printdata_process.join()
