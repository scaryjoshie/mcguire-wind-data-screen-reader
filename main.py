# Imports
import glob
import time
import csv
# Python Imports
from classify_image import adapted_number_prediction, get_crop_values


# Gets images in target folder
TARGET_FOLDER_GLOB = "D:\\Coding\\PathInsights\\mcguire_afb_pole\\Resource folders\\Archive\\*\\*.png"
    #TARGET_FOLDER_GLOB = "input\\*png"
OUTPUT_PATH = "output\\output1.csv"
images_list = glob.glob(TARGET_FOLDER_GLOB)


# Opens crop values and puts into a list
crop1 = "resources\\crop_values_1.csv"
crop2 = "resources\\crop_values_2.csv"
crop_list = [get_crop_values(crop1), get_crop_values(crop2)]


# Runs main
final_list = []
counter = 0
start_time = time.perf_counter()
for image_path in images_list:

    # Gets number and puts in dict
    final_list.append({
        'path': image_path,
        'prediction': adapted_number_prediction(image_path=image_path, crop_list=crop_list)
    })

    # Display stuff
    counter += 1
    print(f"{counter}/{len(images_list)}: {image_path}: {final_list[-1]['prediction']}")


# writes to csv
with open(OUTPUT_PATH, 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames = ['path', 'prediction'], lineterminator = '\n')
    writer.writeheader()
    writer.writerows(final_list)


# Info print
print(f"Successfully processed {len(images_list)} files in {time.perf_counter()-start_time} seconds\nThis makes the speed an average of about {int(len(images_list)/time.perf_counter()-start_time)} files per second")