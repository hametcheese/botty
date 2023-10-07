import cv2
from datetime import datetime
import logging
import os
from pynput import keyboard, mouse
import pyautogui
import time

import screen


DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../data/runs")
os.makedirs(DATA_DIR, exist_ok=True)
time_now = str(datetime.now().strftime("%m-%d-%Y-%H-%M-%S"))
DATA_FILE = os.path.join(DATA_DIR, time_now + ".txt")
logging.basicConfig(filename=DATA_FILE, level=logging.DEBUG)

is_running = True


def on_click(x, y, button, pressed):
    time_now = datetime.now()
    click_str = "click" if pressed else "unclick"
    logging_str = "%s, %s, %s, %s, %s" % (time_now, x, y, button, click_str)
    logging.info(logging_str)


mouse_listener = mouse.Listener(on_click=on_click)
mouse_listener.start()


def on_press(key):
    time_now = datetime.now()
    logging_str = "%s, , , %s, %s" % (time_now, key, "press")
    logging.info(logging_str)
    if key == keyboard.Key.esc:
        global is_running
        is_running = False
        # mouse_listener.stop()
        # return False


def on_release(key):
    time_now = datetime.now()
    logging_str = "%s, , , %s, %s" % (time_now, key, "release")
    logging.info(logging_str)


keyboard_listener = keyboard.Listener(on_press=on_press, on_release=on_release)
keyboard_listener.start()

screen.start_detecting_window()

time.sleep(0.25)

offset_y = screen.monitor_roi["top"]
offset_x = screen.monitor_roi["left"]
first_grab = screen.grab()
x_res = first_grab.shape[0]
y_res = first_grab.shape[1]

VIDEO_FILE = os.path.join(
    DATA_DIR, time_now + "-w%i-h%i-x%i-y%i.mp4" % (x_res, y_res, offset_x, offset_y)
)

# Set the codec and create a VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # Codec for MP4 format
sleep = 0.125
fps = 1.0 / sleep
frame_size = (1920, 1080)  # (width, height)
video_writer = cv2.VideoWriter(VIDEO_FILE, fourcc, fps, frame_size)

while is_running:
    time_now = datetime.now()
    pos = pyautogui.position()
    x, y = pos.x, pos.y
    button = "mouse"
    click_str = "tick"
    logging_str = "%s, %s, %s, %s, %s" % (time_now, str(x), str(y), button, click_str)
    logging.info(logging_str)

    frame = screen.grab()
    video_writer.write(frame)

    time.sleep(sleep)

screen.stop_detecting_window()
video_writer.release()

keyboard_listener.stop()
keyboard_listener.join()
