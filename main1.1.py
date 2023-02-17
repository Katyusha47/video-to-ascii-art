import cv2
import fpstimer
import os
import sys
import time
from multiprocessing import Process
from PIL import Image
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import platform
import moviepy.editor as mp

#ASCII characters
ASCII_CHARS = ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", " "]
frame_size = 150
frame_interval = 1.0 / 30.75
ASCII_LIST = []

#Audio path
def play_audio(path):
    pygame.init()
    pygame.mixer.pre_init(44100, -16, 2, 2048)
    pygame.mixer.init()
    pygame.mixer.music.load(path)
    pygame.mixer.music.play()

#Video path
def play_video(total_frames):
    os.system('color F0')
    os.system('mode 150, 500')

    timer = fpstimer.FPSTimer(30)

    start_frame = 0

    for frame_number in range(start_frame, total_frames):
        sys.stdout.write("\r" + ASCII_LIST[frame_number])
        timer.sleep()

    os.system('color 07')

#Extract frames from video
def extract_transform_generate(video_path, start_frame, number_of_frames=1000):
    capture = cv2.VideoCapture(video_path)
    capture.set(1, start_frame)  # Points cap to target frame
    current_frame = start_frame
    frame_count = 1
    ret, image_frame = capture.read()
    while ret and frame_count <= number_of_frames:
        ret, image_frame = capture.read()
        try:
            image = Image.fromarray(image_frame)
            ascii_characters = pixels_to_ascii(greyscale(resize_image(image)))  # get ascii characters
            pixel_count = len(ascii_characters)
            ascii_image = "\n".join(
                [ascii_characters[index:(index + frame_size)] for index in range(0, pixel_count, frame_size)])

            ASCII_LIST.append(ascii_image)
        except:
            pass
        frame_count += 1
        current_frame += 1
        capture.set(1, current_frame)

    capture.release()

#progress bar
def progress_bar(current, total, bar_length=20):
    progress = float(current) * 100 / total
    arrow = '#' * int(progress / 100 * bar_length - 1)
    spaces = ' ' * (bar_length - len(arrow))
    sys.stdout.write("\rProgress: [%s%s] %d%% Frames %".format(arrow + spaces, int(progress)))

