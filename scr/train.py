import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.callbacks import TensorBoard
from tensorflow.keras.applications import InceptionResNetV2
from tensorflow.keras.layers import Dense, Dropout, Flatten, Input

from load_data import get_train_test_data


x_train, x_test, y_train, y_test = get_train_test_data()

inception_resnet = InceptionResNetV2(weights="imagenet", include_top=False, input_tensor=Input(shape=(224,224,3)))
# ---------------------
headmodel = inception_resnet.output
headmodel = Flatten()(headmodel)
headmodel = Dense(500, activation="relu")(headmodel)
headmodel = Dense(250, activation="relu")(headmodel)
headmodel = Dense(4, activation='sigmoid')(headmodel)


# ---------- model
model = Model(inputs=inception_resnet.input, outputs=headmodel)

# Complie model
model.compile(loss='mse', optimizer=tf.keras.optimizers.Adam(learning_rate=1e-4))
model.summary()

tfb = TensorBoard('object_detection')
history = model.fit(x=x_train, y=y_train, batch_size=10, epochs=180, validation_data=(x_test,y_test), callbacks=[tfb])

model.save('./object_detection.h5')

# Load model
model = tf.keras.models.load_model('./object_detection.h5')
print('Model loaded Sucessfully')
