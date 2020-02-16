import cv2 as cv
import os
import drawer
import math
import numpy as np

def find_ellipses(contours):
    ellipses = [cv.fitEllipse(contour) for contour in contours]
    return ellipses

def remove_small_contours(contours, minimum_area):
    keep_contours = [contour for contour in contours if cv.contourArea(contour) >= minimum_area]
    discard_contours = [contour for contour in contours if cv.contourArea(contour) < minimum_area] 
    return keep_contours, discard_contours

# def separate_ellipsis(contours, minimum_rate=0):
#     # ellipses = cv.fitEllipse(contours[0])
#     return [cv.fitEllipse(contour) for contour in contours]

def distance(point_a, point_b):
    square_x = (point_a[0] - point_b[0])**2
    square_y = (point_a[1] - point_b[1])**2
    return math.sqrt(square_x+square_y)

def find_closest_pair(contour, min_position_distance, precision=1):

    if min_position_distance < 1:
        raise ValueError("Minimum position distance must be greater than zero")
    
    number_points = contour.shape[0]
    closest_pair=None
    closest_distance=99999999
    for index_a  in range(0, number_points, precision):
        point_a = contour[index_a][0]
        
        index_b_start = index_a + min_position_distance
        index_b_end = number_points + index_a - min_position_distance if index_a < min_position_distance else number_points 
        
        for index_b in range(index_b_start, index_b_end, precision):
            point_b = contour[index_b][0]
            pair_distance = distance(point_a, point_b)
            if pair_distance < closest_distance:
                closest_distance = pair_distance
                closest_pair = (index_a, index_b)
    return closest_pair

def separate_contour(contour):
    index_a, index_b = find_closest_pair(contour, 20)
    contour_a = contour[index_a: index_b]
    contour_b =  np.concatenate((contour[index_b:], contour[0:index_a]))
    
    return contour_a, contour_b
    
def break_contours_threshold(contours, max_area):
    final_contours = []
    while contours:
        contours, small_contours = remove_small_contours(contours, max_area)
        final_contours += small_contours
        new_contours_found = []
        for contour in contours:
            print(len(contours))
            print(cv.contourArea(contour))
            contour_a, contour_b = separate_contour(contour)
            print(cv.contourArea(contour_a))
            print(cv.contourArea(contour_b))
            new_contours_found += [contour_a, contour_b]
        contours = new_contours_found
    return final_contours         
def egg_count(filename):
    src_image = cv.imread(filename, 1)
    
    blur_image = cv.GaussianBlur(src_image, (3,3), 0)
    gray_image = cv.cvtColor(blur_image, cv.COLOR_BGR2GRAY)
    _, threshold_image = cv.threshold(gray_image, 200, 255, cv.THRESH_BINARY)

    contours, hierarchy = cv.findContours(threshold_image, cv.CHAIN_APPROX_NONE, cv.RETR_LIST)

    contours, discarded_contours = remove_small_contours(contours, 1500)
    
    contours = break_contours_threshold(contours, 7000)

    index_a, index_b = find_closest_pair(contours[0], 30, precision=15)

    
    print("Index")
    print(contours[0])
    print(index_a)
    print(index_b)
    print(contours[0].shape)
    print(contours[0][index_a][0])
    print(contours[0][index_b][0])
    # ellipses = separate_ellipsis(contours)
    
    # for ellipse in ellipses:
    #     cv.ellipse(src_image, ellipse, (0,0,255), 4)

    # print(contours)
    print("Discarding %d out of %d" %  (len(contours), len(discarded_contours) + len(contours)))
#    ellipses = find_ellipses(contours)
#    ellipses = cf.fitEllipse(contours)

    output_dir = "output/"
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
        
    print("Storing images")
    cv.imwrite(output_dir + "/src.png", src_image)
    cv.imwrite(output_dir + "/blur.png", blur_image)
    cv.imwrite(output_dir + "/gray.png", gray_image)
    cv.imwrite(output_dir + "/threshold.png", threshold_image)

    print("Drawing contours")
    # cv.drawContours(src_image, contours, -1, (200,0,0))
    # cv.drawContours(blur_image, contours, -1, (200,0,0))
    # cv.drawContours(gray_image, contours, -1, (200,0,0))
    cv.drawContours(threshold_image, discarded_contours, -1, (200,0,0), 3)

    print("Drawing discarded contours")
    drawer.draw_contours(src_image, discarded_contours, (0,255,0), width=9)
    drawer.draw_contours(src_image, big_contours, repeat_color=False, width=9)
    drawer.draw_contours(src_image, contours, width=9)

    print("Storing images with contours")
    cv.imwrite(output_dir + "/src_contour.png", src_image)
    cv.imwrite(output_dir + "/blur_contour.png", blur_image)
    cv.imwrite(output_dir + "/gray_contour.png", gray_image)
    cv.imwrite(output_dir + "/threshold_contour.png", threshold_image)

    return