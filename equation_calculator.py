import cv2
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.preprocessing import image
from sympy import *

def binarize(img):
    img = image.img_to_array(img, dtype='uint8')
    binarized = np.expand_dims(cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,11,2), -1)
    inverted_binary_img = ~binarized
    return inverted_binary_img

data_dir = 'data'
batch_size = 32
img_height = 45
img_width = 45

class_names = ['(',
 ')',
 '+',
 '-',
 '0',
 '1',
 '2',
 '3',
 '4',
 '5',
 '6',
 '7',
 '8',
 '9',
 '=',
 'X',
 'cos',
 'div',
 'log',
 'sin',
 'tan',
 'times',
 'y',
 'z']

def getOverlap(a, b):
     return max(0, min(a[1], b[1]) - max(a[0], b[0]))

def detect_contours(img_path):
    input_image = cv2.imread(img_path, 0) # Load a greyscale image
 
    input_image_cpy = input_image.copy()

    binarized = cv2.adaptiveThreshold(input_image_cpy,255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,11,2)
    inverted_binary_img = ~binarized

    contours_list, hierarchy = cv2.findContours(inverted_binary_img,
                                           cv2.RETR_TREE,
                                           cv2.CHAIN_APPROX_SIMPLE) # Find contours
    l = []
    for c in contours_list:
        x, y, w, h = cv2.boundingRect(c)
        l.append([x, y, w, h])
    lcopy = l.copy()
    keep = []
    while len(lcopy) != 0:
        curr_x, curr_y, curr_w, curr_h = lcopy.pop(0) # Look at next box
        if curr_w * curr_h < 20: # remove very small boxes
            continue
        throw = []
        for i, (x, y, w, h) in enumerate(lcopy):
            curr_interval = [curr_x, curr_x+curr_w]
            next_interval = [x, x+w]
            if getOverlap(curr_interval, next_interval) > 1 : # more than 3 pixels overlap, this is arbitrary
                # Merge the two intervals
                new_interval_x = [min(curr_x, x), max(curr_x+curr_w, x+w)]
                new_interval_y = [min(curr_y, y), max(curr_y+curr_h, y+h)]
                newx, neww = new_interval_x[0], new_interval_x[1] - new_interval_x[0]
                newy, newh = new_interval_y[0], new_interval_y[1] - new_interval_y[0]
                curr_x, curr_y, curr_w, curr_h = newx, newy, neww, newh
                throw.append(i) # Mark this box to throw away later, since it has now been merged with current box
        for ind in sorted(throw, reverse=True): # Sort in reverse order otherwise we will pop incorrectly
            lcopy.pop(ind)
        keep.append([curr_x, curr_y, curr_w, curr_h]) # Keep the current box we are comparing against
    return keep

def resize_pad(img, size, padColor=255):

    h, w = img.shape[:2]
    sh, sw = size

    # interpolation method
    if h > sh or w > sw: # shrinking image
        interp = cv2.INTER_AREA
    else: # stretching image
        interp = cv2.INTER_CUBIC

    # aspect ratio of image
    aspect = w/h  # if on Python 2, you might need to cast as a float: float(w)/h

    # compute scaling and pad sizing
    if aspect > 1: # horizontal image
        new_w = sw
        new_h = np.round(new_w/aspect).astype(int)
        pad_vert = (sh-new_h)/2
        pad_top, pad_bot = np.floor(pad_vert).astype(int), np.ceil(pad_vert).astype(int)
        pad_left, pad_right = 0, 0
    elif aspect < 1: # vertical image
        new_h = sh
        new_w = np.round(new_h*aspect).astype(int)
        pad_horz = (sw-new_w)/2
        pad_left, pad_right = np.floor(pad_horz).astype(int), np.ceil(pad_horz).astype(int)
        pad_top, pad_bot = 0, 0
    else: # square image
        new_h, new_w = sh, sw
        pad_left, pad_right, pad_top, pad_bot = 0, 0, 0, 0

    # set pad color
    if len(img.shape) == 3 and not isinstance(padColor, (list, tuple, np.ndarray)): # color image but only one color provided
        padColor = [padColor]*3

    # scale and pad
    scaled_img = cv2.resize(img, (new_w, new_h), interpolation=interp)
    scaled_img = cv2.copyMakeBorder(scaled_img, pad_top, pad_bot, pad_left, pad_right, borderType=cv2.BORDER_CONSTANT, value=padColor)

    return scaled_img

def put_double_asterisk(s):
    lst = list(s)
    i = 0
    while i < len(lst)-1:
        if lst[i]=='x' or lst[i]=='y' or lst[i]=='z' or lst[i]=='X' or lst[i]=='Y' or lst[i]=='Z':
            if lst[i+1].isdigit():
                lst.insert(i+1, '**')
                i += 1
        i += 1
    s_new = ''.join(lst)
    return s_new

def put_single_asterisk(s):
    lst = list(s)
    i=0
    while i < len(lst)-1:
        if lst[i].isdigit() and lst[i+1].isalpha():
            lst.insert(i+1,'*')
        i+=1
    s_new = ''.join(lst)
    return s_new 

    
# Kepp your trained model path here.
new_model = tf.keras.models.load_model('eqn-detect18-model', compile=False)

def equation_solver_function(img_path):

    flag = 0
    IMAGE = img_path.split('\\')[-1]

    img_path = "static/"+IMAGE
    image_dir = "static/"

    if flag == 1:
        input_image = cv2.imread(img_path) 
        ret, bw_img = cv2.threshold(input_image,127,255,cv2.THRESH_BINARY)
        plt.imshow(bw_img)
        plt.show()
        cv2.imwrite(img_path, bw_img) 
        keep = detect_contours(image_dir+IMAGE)
        img_path = image_dir+IMAGE
    else:
        input_image = cv2.imread(img_path, 0) 
        keep = detect_contours(image_dir+IMAGE)


    eqn_list = []
    input_image = cv2.imread(img_path, 0) 
    inverted_binary_img = binarize(input_image)
    for (x, y, w, h) in sorted(keep, key = lambda x: x[0]):
        img = resize_pad(inverted_binary_img[y:y+h, x:x+w], (45, 45), 0) # We must use the binarized image to predict
        first = tf.expand_dims(img, 0)
        second = tf.expand_dims(first, -1)
        predicted = new_model.predict(second)
        max_arg = np.argmax(predicted)
        pred_class = class_names[max_arg]
        if pred_class == "times":
            pred_class = "*"
        if pred_class == "div":
            pred_class = chr(47)
        eqn_list.append(pred_class)
      
    eqn = "".join(eqn_list)
    equation = put_double_asterisk(eqn)
    equation = put_single_asterisk(equation)

    return equation




