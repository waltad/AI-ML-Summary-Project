# import os
# import cv2
import numpy as np
import pandas as pd
# import tensorflow as tf
# import pytesseract as pt
# import plotly.express as px
# import matplotlib.pyplot as plt
import xml.etree.ElementTree as xet

from glob import glob
from utils import extract_image_coordinates_from_xml_to_dict, get_image_path, data_normalize
# from skimage import io
# from shutil import copy
# from tensorflow.keras.models import Model
# from tensorflow.keras.callbacks import TensorBoard
from sklearn.model_selection import train_test_split
# from tensorflow.keras.applications import InceptionResNetV2
# from tensorflow.keras.layers import Dense, Dropout, Flatten, Input
# from tensorflow.keras.preprocessing.image import load_img, img_to_array


def get_train_test_data():
    path = glob('data/images/*.xml')

    df = pd.DataFrame(extract_image_coordinates_from_xml_to_dict(path))

    df.to_csv('labels.csv', index=False)
    print(df.head())

    license_plate_coordinate = df.iloc[:,1:].values

    image_path_list = list(df['filepath'].apply(get_image_path))
    print(image_path_list[:10])

    data_image_normalize, output_cordinate_normalize = data_normalize(license_plate_coordinate, image_path_list)

    # Convert data to array
    X = np.array(data_image_normalize, dtype=np.float32)
    y = np.array(output_cordinate_normalize, dtype=np.float32)
    print(X.shape, y.shape)

    # Split the data into training and testing set using sklearn.
    x_train, x_test, y_train, y_test = train_test_split(X, y, train_size=0.8, random_state=0)
    print(x_train.shape, x_test.shape,y_train.shape, y_test.shape)

    return x_train, x_test, y_train, y_test
