import xml.etree.ElementTree as xet
import os
import cv2
from tensorflow.keras.preprocessing.image import load_img, img_to_array


def extract_image_coordinates_from_xml_to_dict(path):
    
    labels_dict = dict(filepath=[],xmin=[],xmax=[],ymin=[],ymax=[])

    for filename in path:
        info = xet.parse(filename)
        root = info.getroot()
        member_object = root.find('object')
        labels_info = member_object.find('bndbox')
        xmin = int(labels_info.find('xmin').text)
        xmax = int(labels_info.find('xmax').text)
        ymin = int(labels_info.find('ymin').text)
        ymax = int(labels_info.find('ymax').text)

        labels_dict['filepath'].append(filename)
        labels_dict['xmin'].append(xmin)
        labels_dict['xmax'].append(xmax)
        labels_dict['ymin'].append(ymin)
        labels_dict['ymax'].append(ymax)

    return labels_dict


def get_image_path(path_to_xml):
    filename_image = xet.parse(path_to_xml).getroot().find('filename').text
    filepath_image = os.path.join('data/images', filename_image)
    return filepath_image



def data_normalize(license_plate_coordinates, image_path_list):
    
    # labels = df.iloc[:,1:].values
    data = []
    output = []
    
    for ind in range(len(image_path_list)):
        image = image_path_list[ind]
        img_arr = cv2.imread(image)
        h, w, d = img_arr.shape
        # Prepprocesing
        load_image = load_img(image,target_size=(224,224))
        load_image_arr = img_to_array(load_image)
        norm_load_image_arr = load_image_arr/255.0 # Normalization
        # Normalization to labels
        xmin, xmax, ymin, ymax = license_plate_coordinates[ind]
        nxmin, nxmax = xmin/w, xmax/w
        nymin, nymax = ymin/h, ymax/h
        label_norm = (nxmin,nxmax,nymin,nymax) # Normalized output
        # Append
        data.append(norm_load_image_arr)
        output.append(label_norm)

    return data, output
    