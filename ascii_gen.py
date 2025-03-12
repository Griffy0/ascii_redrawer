import imageio.v2 as iio
import cv2
import math
from colorama import Fore
from colorama import init
import argparse
import glob
from random import choice
import os

def rgb_to_brightness(rgb):
    avg = sum(rgb)/3
    normalized_rgb = int(avg / 51-0.5)
    return max(normalized_rgb,0)

def rgb_to_char(rgb,chars):
    brightness = rgb_to_brightness(rgb)
    return chars[brightness]

def rgb_to_colour(rgb):
    normalized_rgb = [int(x / 51) for x in rgb]
    return f"\x1b[38;5;{16 + 36 * normalized_rgb[0] + 6 * normalized_rgb[1] + normalized_rgb[2]}m"


def resize_img(img, width, height):
    #find whether width or height is larger
    img_height = img.shape[0]
    img_width = img.shape[1]
    aspect_ratio = img_width/img_height
    intended_ratio = width/height
    center_width = math.floor(img_width/2)
    center_height = math.floor(img_height/2)
    ratio_diff = intended_ratio/aspect_ratio

    if (ratio_diff<1):
        #width too big
        total_width  = img_width * (ratio_diff)
        total_height = img_height
    else:
        #too high
        total_width  = img_width
        total_height = img_height/ratio_diff

    half_width = math.floor(total_width/2)
    half_height = math.floor(total_height/2)
    cropped = img[center_height-half_height:center_height+half_height,center_width-half_width:center_width+half_width]
    return cropped

def print_img(img):
    chars = [' ', '.', '*', '$', '#']
    out = []
    for i in img:
        for j in i:
            col = rgb_to_colour(j)
            char = rgb_to_char(j, chars)
            out.append(col+char)
        out.append('\n')

    out_str = ''.join(out)
    print(out_str)
    print(Fore.WHITE)

def render_file(file, width, height):

    if file == 'random':
        files = glob.glob((f'{os.path.dirname(__file__)}/*.png'))
        file = choice(files)

    img = iio.imread(file)
    text_height = 1.5
    cropped = resize_img(img, width, round(height*text_height))
    resized = cv2.resize(cropped, (width, int(height/text_height)))

    print_img(resized)    

    init()

parser = argparse.ArgumentParser()

parser.add_argument('filename')
parser.add_argument('width')
parser.add_argument('height')

args = parser.parse_args()
render_file(args.filename, int(args.width), int(args.height))  
