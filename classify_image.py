# Imports
from PIL import Image
import csv
import glob
import random
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np
import cv2
# Python imports
from mask_image import MaskImage


# List of possible mutable strings
mutable_string_dict = {
    "1110111": "0",
    "0100100": "1",
    "1101011": "2",
    "1101101": "3",
    "0111100": "4",
    "1011101": "5",
    "1011111": "6",
    "1100100": "7",
    "1111111": "8",
    "1111101": "9",
    "0000000": "",
}


# Function to predict the digit using the mutable string dict above
def predict_digit(mutable_string):

    # Checks if both tens and ones digits check out
    if mutable_string == "00000000000000": # The case where there are no digits detected
        return 'None'
    
    elif mutable_string[:7] in mutable_string_dict.keys() and mutable_string[7:] in mutable_string_dict.keys(): # The case where everything is normal
        tens_digit = mutable_string_dict[mutable_string[:7]]
        ones_digit = mutable_string_dict[mutable_string[7:]]
        return tens_digit + ones_digit
    
    else: # All edge cases
        return 'None'



# Function to return the dominant color of an image. Currently set so that as long as over 1/5 of the pixels are black, the digit stem "counts"
def get_binary_value(cropped_image, dominance_ratio = 0.2): # dominance ratio = allowed ratio of black:total pixels for the image to count as a digit stem
    # Converts cropped PIL image to a cv2 image
    img = cv2.cvtColor(np.array(cropped_image), cv2.COLOR_RGB2BGR)
    
    # Gets image
    number_of_white_pix = np.sum(img == 255)
    number_of_black_pix = np.sum(img == 0)

    # Returns
    if number_of_black_pix/(number_of_black_pix + number_of_white_pix) > dominance_ratio:
        return "1"
    else:
        return "0"



# Function to read and get crop values from the crop values file
def get_crop_values(path='resources\\crop_values_2.csv'):
    with open(path, 'r') as f:
        # Gets data as list
        reader = csv.reader(f)
        data = [list(row) for row in reader]
        data.pop(0) # removes label items

        crop_dict = {} # empty dict that will be filled
        # Reads into dict
        for i in data:

            # Gets crop values as tuple
            crop_list = i[2:]
            crop_values_as_int = [int(x) for x in crop_list]
            crop_values_tuple = tuple(crop_values_as_int)
            crop_dict[i[1]] = crop_values_tuple
        
        # Returns 
        return crop_dict
    


def get_image_num(path, crop_values, overlay_mode=False):

    # Opens image
    im = Image.open(path) 
    # Masks image
    masked_image = MaskImage(im=im)

    # Shows image
    if overlay_mode == True:
        plt.imshow(masked_image, cmap="gray")
    
    # Turns masked image (numpy array) into a PIL image object
    image_from_array = Image.fromarray(masked_image)

    # Creates a string to mutate
    mutable_string = ""

    # Creates mutable string to test against digit values
    for section in crop_values.keys():

        # Overlay
        if overlay_mode == True:
            plt.gca().add_patch(Rectangle(
            (crop_values[section][0],crop_values[section][1]), crop_values[section][2] - crop_values[section][0], crop_values[section][3] - crop_values[section][1],
            linewidth=2,edgecolor='r',facecolor='none'))
    
        # Crops image
        cropped_image = image_from_array.crop(crop_values[section])

        # Adds binary value to mutable string
        binary_value = get_binary_value(cropped_image)
        mutable_string = mutable_string + binary_value
    
    # Shows plot
    if overlay_mode == True:
        plt.show()
    
    # Returns digit prediction
    return predict_digit(mutable_string=mutable_string)



# Function becuase numbers are somehow on different elevations sometimes
def adapted_number_prediction(image_path, crop_list):
    num = get_image_num(path=image_path, crop_values=crop_list[0], overlay_mode=False)
    if num == None or num == 'None':
        num = get_image_num(path=image_path, crop_values=crop_list[1], overlay_mode=False)
    return num




######################## Run this if you want to see the number overlay
if __name__ == "__main__":

    DIR_PATH = "D:\\Coding\\PathInsights\\mcguire_afb_pole\\Resource folders\\mcguire afb pole 2\\output2\\*.png"
    DIR_PATH_2 = "D:\\Coding\\PathInsights\\mcguire_afb_pole\\Resource folders\\wind speeds 0 to 20\\wind speeds 0 to 20\\*.png"
    DIR_PATH_3 = "D:\\Coding\\PathInsights\\mcguire_afb_pole\\Resource folders\\Archive\\*\\*.png"

    # Gets image list
    images_list = glob.glob(DIR_PATH_3)

    # Gets crop values
    crop_values = get_crop_values(path="resources\\crop_values_1.csv")
    #print(crop_values)


    while True:
        
        # Chooses and opens a random image
        path = random.choice(images_list)
        print(path)

        # Gets and prints image num
        print(get_image_num(path=path, crop_values=crop_values, overlay_mode=True))