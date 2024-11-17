import kagglehub
trainingdatapro_license_plates_1_209_438_ocr_plates_path = kagglehub.dataset_download('trainingdatapro/license-plates-1-209-438-ocr-plates')

print('Data source import complete.')

import os
import shutil
from pprint import pprint
import matplotlib.pyplot as plt
import cv2
import pandas as pd

par_dir = 'data' #'/kaggle/input/license-plates-1-209-438-ocr-plates'

df = pd.read_csv(f'{par_dir}/for_notebook/data_cars.csv')
df.head(1)