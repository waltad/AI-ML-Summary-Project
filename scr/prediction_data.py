import tensorflow as tf
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import numpy as np
import plotly.express as px


# Load model
model = tf.keras.models.load_model('./models/license_plate_frame_recognition_model.keras')
print('Model loaded Sucessfully')

path = 'data/TEST/TEST.jpeg'
image = load_img(path) # PIL object
image = np.array(image,dtype=np.uint8) # 8 bit array (0,255)
image1 = load_img(path,target_size=(224,224))
image_arr_224 = img_to_array(image1)/255.0  # Convert into array and get the normalized output

# Size of the orginal image
h,w,d = image.shape
print('Height of the image =',h)
print('Width of the image =',w)

# fig = px.imshow(image)
# fig.update_layout(width=700, height=500,  margin=dict(l=10, r=10, b=10, t=10), xaxis_title='Figure 13 - TEST Image')

test_arr = image_arr_224.reshape(1,224,224,3)

coords = model.predict(test_arr)

print(coords)

denorm = np.array([w,w,h,h])
coords = coords * denorm
coords = coords.astype(np.int32)
print('Denormalized coordinates:', coords)