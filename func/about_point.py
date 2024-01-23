def xyxy2xywh(xyxy):
    x1, y1, x2, y2 = xyxy
    w = max(x1, x2) - min(x1, x2)
    h = max(y1, y2) - min(y1, y2)
    x1 = min(x1, x2)
    y1 = min(y1, y2)
    return x1, y1, w, h
