import tensorflow as tf
from tensorflow.keras.models import Model
import datetime
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
model.compile(
    loss='mse',
    optimizer=tf.keras.optimizers.Adam(learning_rate=1e-4),
    metrics=['accuracy']
    )
model.summary()

# tensorboard --logdir logs/fit
# tensorboard --logdir logs/gradient_tape
log_dir = "logs/fit/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1)
history = model.fit(x=x_train, y=y_train, batch_size=10, epochs=180, validation_data=(x_test,y_test), callbacks=[tensorboard_callback])

# In order for the model to be saved, you must create a directory called "models"
model.save('./models/object_detection.keras')

# Load model
model = tf.keras.models.load_model('./models/object_detection.keras')
print('Model loaded Sucessfully')
