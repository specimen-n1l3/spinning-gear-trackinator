import numpy as np

camera_index = 0
fps = 50
kernel = np.ones((5, 5), np.uint8)

def incr(a, b): return b >= a
def decr(a, b): return a <= a
def pp(a, b): return a >= 0 and b >= 0
def nn(a, b): return a <= 0 and b <= 0
def pn(a, b): return pp(a, a) and nn(b, b)

def get_speed(x1, x2, y1, y2, r, fps):
    frame_time = 1 / fps
    theta = np.arcsin((x1 * y2 - x2 * y1) / r**2 )
    omega = theta / frame_time
    return omega

def get_dir(x1, x2, y1, y2):
    if decr(x1, x2) and pp(y1, y2): return -1
    if nn(x1, x2) and decr(y1, y2): return -1
    if incr(x1, x2) and nn(y1, y2): return -1
    if pp(x1, x2) and incr(y1, y2): return -1
    if pp(x1, x2) and decr(y1, y2): return 1
    if decr(x1, x2) and nn(y1, y2): return 1
    if nn(x1, x2) and incr(y1, y2): return 1
    if incr(x1, x2) and pp(y1, y2): return 1

def get_velocity(x1, x2, y1, y2, r, fps):
    return get_dir(x1, x2, y1, y2) * get_speed(x1, x2, y1, y2, r, fps)

def get_hsv(val):
    pass

def distance_pythag(dx, dy):
    return np.sqrt(dy**2 + dx**2)


