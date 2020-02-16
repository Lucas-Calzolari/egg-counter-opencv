import cv2 as cv
from random import randint

def get_random_color():
    return (randint(0, 255), randint(0, 255), randint(0, 255))

def draw_contours(image, contours, color=None, repeat_color=True, width=3):
    if color is not None and repeat_color == False:
        raise ValueError("If repeat is false, then color must be either none or an array")

    if repeat_color:
        if color is None:
            color = get_random_color()
        cv.drawContours(image, contours, -1, color, width)    
    else:
        for contour in contours:
            color = get_random_color()
            cv.drawContours(image, [contour], -1, color, width)