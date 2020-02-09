import cv2 as cv
import os

def find_ellipses(contours):
    ellipses = [cv.fitEllipse(contour) for contour in contours]
    return ellipses

def find_contours(bw_image):
    _, contours = cv.findContours(bw_image, cv.CHAIN_APPROX_NONE, cv.RETR_EXTERNAL)
    return contours

def egg_count(filename):
    src_image = cv.imread(filename, 1)
    blur_image = cv.GaussianBlur(src_image, (15,15), 0)
    gray_image = cv.cvtColor(blur_image, cv.COLOR_BGR2GRAY)
    _, threshold_image = cv.threshold(gray_image, 200, 255, cv.THRESH_BINARY)

    contours = find_contours(threshold_image)
#    ellipses = find_ellipses(contours)
#    ellipses = cf.fitEllipse(contours)

    output_dir = "output/"
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
        
    cv.imwrite(output_dir + "/src.png", src_image)
    cv.imwrite(output_dir + "/blur.png", blur_image)
    cv.imwrite(output_dir + "/gray.png", gray_image)
    cv.imwrite(output_dir + "/threshold.png", threshold_image)

    #cv.drawContours(src_image, contours, -1, (200,0,0))
    #cv.drawContours(blur_image, contours, -1, (200,0,0))
    #cv.drawContours(gray_image, contours, -1, (200,0,0))
    cv.drawContours(threshold_image, contours, -1, (200,0,0))
    
    #cv.imwrite(output_dir + "/src_contour.png", src_image)
    #cv.imwrite(output_dir + "/blur_contour.png", blur_image)
    #cv.imwrite(output_dir + "/gray_contour.png", gray_image)
    cv.imwrite(output_dir + "/threshold_contour.png", threshold_image)

    return