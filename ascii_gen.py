import imageio as iio
import cv2
import math
from colorama import Fore
from colorama import init
import argparse

def rgb_to_brightness(rgb):
    normalized_rgb = [x / 255 for x in rgb]
    return max(sum(normalized_rgb)/len(rgb)-0.1,0)



def rgb_to_char(rgb):
    chars = [' ', '.', '*', '$', '#']
    num_chars = len(chars)
    brightness = rgb_to_brightness(rgb)
    index = math.ceil(brightness*num_chars)-1
    return chars[index]


def get_distance_colour(colour1, colour2):
    
    return sum([abs(int(x) - int(y)) for x, y in zip(colour1, colour2)])

def rgb_to_colour(rgb):
    codes = [
        [-40,  -40,  -40], 
        [255,0,  0], 
        [0,  255,0], 
        [255,255,0], 
        [0,  0,  255],
        [255,0,  255], 
        [0,  255,255],
        [255,255,255]   
    ]
    names = [
        Fore.BLACK,
        Fore.RED,
        Fore.GREEN,
        Fore.YELLOW,
        Fore.BLUE,
        Fore.MAGENTA,
        Fore.CYAN,
        Fore.WHITE
        ]

    closest = 99999
    closest_index = 0
    for i, item in enumerate(codes):
        distance = get_distance_colour(rgb, item)
        if distance < closest:
            closest = distance
            closest_index = i
    return names[closest_index]


def render_file(file, width, height):
    out = []

    img = iio.imread(file)
    center = [x/2 for x in img.shape]
    intended_ratio = 1
    smallest = min(img.shape[0]*intended_ratio, img.shape[1])
    print(img.shape)
    cropped = img[0:smallest, 0:smallest]   
    resized = cv2.resize(cropped, (width, height))

    init()

    print(rgb_to_colour([98, 152, 172])+'asd')


    for i in resized:
        for j in i:
            out.append(rgb_to_colour(j)+rgb_to_char(j))
        out.append('\n')

    out_str = ''.join(out)
    print(out_str)
    print(Fore.WHITE)


parser = argparse.ArgumentParser()

parser.add_argument('filename')
parser.add_argument('width')
parser.add_argument('height')

args = parser.parse_args()
render_file(args.filename, int(args.width), int(args.height))  
