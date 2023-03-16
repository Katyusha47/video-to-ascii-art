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

def resize_image(image_frame):
    width, height = image_frame.size
    aspect_ratio = (height / float(width * 2.5))
    new_height = int(aspect_ratio * frame_size)
    resized_image = image_frame.resize((frame_size, new_height))
    return resized_image

def greyscale(image_frame):
    return image_frame.convert("L")

def pixels_to_ascii(image_frame):
    pixels = image_frame.getdata()
    characters = "".join([ASCII_CHARS[pixel // 25] for pixel in pixels])
    return characters

def ascii_generator(image_frame, start_frame, number_of_frames):
    current_frame = start_frame
    while current_frame <= number_of_frames:
        path_to_image = image_frame + 'frame' + str(current_frame) + '.jpg'
        image = Image.open(path_to_image)
        ascii_characters = pixels_to_ascii(greyscale(resize_image(image)))  # get ascii characters
        pixel_count = len(ascii_characters)
        ascii_image = "\n".join(
            [ascii_characters[index:(index + frame_size)] for index in range(0, pixel_count, frame_size)])
        file_name = r"TextFiles/" + "frame" + str(current_frame) + ".txt"
        try:
            with open(file_name, "w")as f:
                f.write(ascii_image)
        except FileNotFoundError:
            continue
        current_frame += 1

        def preflight_operations(path):
            if os.path.exists(path):
                path_to_video = path.strip()
                cap = cv2.VideoCapture(path_to_video)
                total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                cap.release()

                video = mp.VideoFileClip(path_to_video)
                path_to_audio = r"Audio/" + "audio.mp3"
                video.audio.write_audiofile(path_to_audio)

                frame_per_process = int(total_frames // 4)

                process1_end_frame = frame_per_process
                process2_start_frame = process1_end_frame + 1
                process2_end_frame = process2_start_frame + frame_per_process
                process3_start_frame = process2_end_frame + 1
                process3_end_frame = process3_start_frame + frame_per_process
                process4_start_frame = process3_end_frame + 1
                process4_end_frame = total_frames - 1

                start_time = time.time()
                sys.stdout.write('Generating frames...\n')
                extract_transform_generate(path_to_video, 1, process4_end_frame)








