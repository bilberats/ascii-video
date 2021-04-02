import PIL.Image,PIL.ImageDraw,PIL.ImageFont,PIL.ImageEnhance
import cv2
import os
import time


#ascii chars
ASCII_CHARS = "@%#*+=-:. "

#resize
def resize_image(image,new_width):
    width, height = image.size
    ratio = height / width / 2
    new_height = int(new_width*ratio)
    resized_image = image.resize((new_width, new_height))
    return resized_image

#convert each pixel to grayscale
def grayify(image):
    grayscale_image = image.convert("L")
    sharp = PIL.ImageEnhance.Sharpness(grayscale_image)
    grayscale_image = sharp.enhance(3)
    contrast = PIL.ImageEnhance.Contrast(grayscale_image)
    grayscale_image = contrast.enhance(1)
    return grayscale_image

#convert pixels to ascii
def pixel_to_ascii(image):
    pixels = image.getdata()
    characters = "".join([ASCII_CHARS[int(pixel//(255/(len(ASCII_CHARS)-1)))] for pixel in pixels])
    return characters


def imagetoascii(image,new_width):
    #convert image to ascii
    new_image_data = pixel_to_ascii(grayify(resize_image(image,new_width)))

    #format
    pixel_count = len(new_image_data)
    ascii_image = "\n".join(new_image_data[i:(i+new_width)] for i in range(0, pixel_count, new_width))

    return ascii_image


def getFrame(sec,vidcap):
    vidcap.set(cv2.CAP_PROP_POS_MSEC,sec*1000)
    hasFrames,image = vidcap.read()

    return hasFrames,image



def main(vidcap,quality,framerate):
    vidcap = cv2.VideoCapture(vidcap)
    frameduration = 1/framerate
    sec = 0
    time1 = time.time()
    success = True
    success,image = getFrame(sec,vidcap)
    while success:
        cv2.imwrite("temp.jpg", image)
        image = PIL.Image.open("temp.jpg")
        printing= imagetoascii(image,quality)
        sec += frameduration
        sec = round(sec, 2)
        time2 = time.time()
        timediference = time2-time1
        time1 = time.time()
        if timediference < frameduration:
            time.sleep(frameduration-timediference)
        os.system('cls' if os.name == 'nt' else 'clear')
        print(printing)
        success,image = getFrame(sec,vidcap)

if __name__=='__main__':
    vidcap = input(str("Video name path:"))
    main(vidcap,150,5)
