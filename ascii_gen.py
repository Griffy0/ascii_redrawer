import imageio.v2 as iio
import cv2
import math
from colorama import Fore
from colorama import init
import argparse
import glob
from random import choice
import os
from line_profiler import profile

def rgb_to_brightness(rgb):
    normalized_rgb = [x / 255 for x in rgb]
    return max(sum(normalized_rgb)/len(rgb)-0.1,0)

@profile
def rgb_to_char(rgb):
    chars = [' ', '.', '*', '$', '#']
    num_chars = len(chars)
    brightness = rgb_to_brightness(rgb)
    index = math.ceil(brightness*num_chars)-1
    return chars[index]

@profile
def get_distance_colour(colour1, colour2):
    return sum([abs(int(x) - int(y)) for x, y in zip(colour1, colour2)])

@profile
def rgb_to_colour(rgb, codes, names):
    #return f"\033[38;2;{rgb[0]};{rgb[1]};{rgb[2]}m"
    closest = 2000
    closest_index = 0
    for i, item in enumerate(codes):
        distance = get_distance_colour(rgb, item)
        if distance < closest:
            closest = distance
            closest_index = i
    return names[closest_index]

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

@profile
def print_img(img):
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
    out = []
    for i in img:
        for j in i:
            col = rgb_to_colour(j, codes, names)
            char = rgb_to_char(j)
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
    #cv2.imshow('image',cropped)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()


parser = argparse.ArgumentParser()

parser.add_argument('filename')
parser.add_argument('width')
parser.add_argument('height')

args = parser.parse_args()
render_file(args.filename, int(args.width), int(args.height))  
