import cv2
import fpstimer
import os
import sys
import time
from PIL import Image
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import platform

#ASCII characters
ASCII_CHARS = ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", " "]
frame_size = 150
frame_interval = 1.0 / 30.75
ASCII_LIST = []

#read ASCII characters
def video(end_frame):
    if platform.system() == 'Windows':
        os.system('color F0')
        time.sleep(0)
    elif platform.system() == 'Linux':
        time.sleep(0.4)

    timer = fpstimer.FPSTimer(30)

    if end_frame:
        start_frame = 1
    else:
        start_frame = 0

    for frame_number in range(start_frame, end_frame-1):
        sys.stdout.write("\r" + ASCII_LIST[frame_number])
        timer.sleep()

    sys.stdout.write("\n")
    os.system('color 07')

#extract frames from video
def extract_transform_generate(video, start_frame, number_of_frames=1000):
    capture = cv2.VideoCapture(video)
    capture.set(1, start_frame)
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

        except Exception as error:
            continue

        progress_bar(frame_count, number_of_frames)
        frame_count += 1
        current_frame += 1

    capture.release()


def audio(path):
    pygame.init()
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.mixer.init()
    pygame.mixer.music.load(path)
    pygame.mixer.music.play()

def progress_bar(current, total, barLength=25):
    progress = float(current) * 100 / total
    arrow = '#' * int(progress / 100 * barLength - 1)
    spaces = ' ' * (barLength - len(arrow))
    sys.stdout.write('\rProgress: [%s%s] %d%% Frame %d of %d frames' % (arrow, spaces, progress, current, total))


def resize_image(image_frame):
    width, height = image_frame.size
    aspect_ratio = (height / float(width * 2.5))
    new_height = int(aspect_ratio * frame_size)
    resized_image = image_frame.resize((frame_size, new_height))
    return resized_image


def greyscale(image_frame):
    return image_frame.convert('L')

def pixels_to_ascii(image_frame):
    pixels = image_frame.getdata()
    characters = "".join([ASCII_CHARS[pixel // 25] for pixel in pixels])
    return characters

def ascii_generator(image_path, start_frame, number_of_frames):
    current_frame = start_frame
    while current_frame <= number_of_frames:
        path_to_image = image_path + 'apple_' + str(current_frame) + '.jpg'
        image = Image.open(path_to_image)
        ascii_characters = pixels_to_ascii(greyscale(resize_image(image)))
        pixel_count = len(ascii_characters)
        ascii_image = "\n".join([ascii_characters[index:(index + frame_size)] for index in range(0, pixel_count, frame_size)])
        file_name ="TextFiles/" + "apple" + str(current_frame) + ".txt"
        try:
            with open(file_name, "w") as f:
                f.write(ascii_image)
        except FileNotFoundError:
            continue
        current_frame += 1


def preflight_operations():
    video_path = 'Videos/Apple.mp4'
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.release()

    if not ASCII_LIST:
        start_time = time.time()
        sys.stdout.write('Beginning ASCII generation...\n')
        extract_transform_generate(video_path, 0, total_frames)
        execution_time = time.time() - start_time
        sys.stdout.write('\nASCII generation completed! ASCII generation time: ' + str(execution_time))
        time.sleep(2)
    elif ASCII_LIST:
        sys.stdout.write('ASCII assets found in memory, re-using assets\n')
        time.sleep(2)

    return total_frames


def main():
    while True:
        user_input = input("Input your frame number: (Default: 150) ")
        user_input.strip()

        try:
            global frame_size
            frame_size = int(user_input)
        except:
            sys.stdout.write("Invalid input. Using default frame size: 150")
            frame_size = 150

        sys.stdout.write('[1] Play video\n')
        sys.stdout.write('[2] Exit\n')

        user_input = str(input("Input your choice: "))
        user_input.strip()

        if user_input == '1':
            sys.stdout.write('choose your Audio\n')
            sys.stdout.write('[1] Apple\n')
            sys.stdout.write('[2] Acapella\n')
            user_input = str(input("Input your choice: "))
            user_input.strip()
            if user_input == '1':
                path_to_file = "Audio/Apple.mp3"
                total_frames = preflight_operations()
                audio(path_to_file)
                video(end_frame=total_frames)
            elif user_input == '2':
                path_to_file = "Audio/Acapella.wav"
                total_frames = preflight_operations()
                audio(path_to_file)
                video(end_frame=total_frames)
            else:
                sys.stdout.write('Invalid input. Exiting program...')
                sys.exit()

        elif user_input == '2':
            sys.stdout.write('Exiting program...')
            sys.exit()
        else:
            sys.stdout.write('Invalid input. Exiting program...')
            sys.exit()

if __name__ == '__main__':
    main()
