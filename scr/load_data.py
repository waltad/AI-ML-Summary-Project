# import os
# import cv2
# import numpy as np
import pandas as pd
# import tensorflow as tf
# import pytesseract as pt
# import plotly.express as px
# import matplotlib.pyplot as plt
import xml.etree.ElementTree as xet

from glob import glob
from utils import extract_image_coordinates_from_xml_to_dict
# from skimage import io
# from shutil import copy
# from tensorflow.keras.models import Model
# from tensorflow.keras.callbacks import TensorBoard
# from sklearn.model_selection import train_test_split
# from tensorflow.keras.applications import InceptionResNetV2
# from tensorflow.keras.layers import Dense, Dropout, Flatten, Input
# from tensorflow.keras.preprocessing.image import load_img, img_to_array


path = glob('data/images/*.xml')

df = pd.DataFrame(extract_image_coordinates_from_xml_to_dict(path))

df.to_csv('labels.csv', index=False)
print(df.head())