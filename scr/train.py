import mlflow
import mlflow.tensorflow
import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.metrics import Accuracy
# import datetime
from tensorflow.keras.applications import InceptionResNetV2
from tensorflow.keras.layers import Dense, Dropout, Flatten, Input

from load_data import get_train_test_data


# Load dataset
x_train, x_test, y_train, y_test = get_train_test_data()

mlflow.set_experiment("Object Detection Experiment")

# Enable auto logging - run in terminal: mlflow ui
# Enable automatic logging for TensorFlow
mlflow.tensorflow.autolog()

# Begin an MLflow run
with mlflow.start_run():

    # Define your model
    inception_resnet = InceptionResNetV2(weights="imagenet", include_top=False, input_tensor=Input(shape=(224, 224, 3)))
    headmodel = inception_resnet.output
    headmodel = Flatten()(headmodel)
    headmodel = Dense(500, activation="relu")(headmodel)
    headmodel = Dense(250, activation="relu")(headmodel)
    headmodel = Dense(4, activation='sigmoid')(headmodel)
    model = Model(inputs=inception_resnet.input, outputs=headmodel)

    # Compile the model
    loss = 'mse'
    optimizer = tf.keras.optimizers.Adam(learning_rate=1e-4)
    
    model.compile(
        loss=loss,
        optimizer=optimizer,
        metrics=['accuracy']
    )

    model.summary()

    # Log model parameters
    mlflow.log_param("loss_function", loss)
    mlflow.log_param("optimizer", "Adam")
    mlflow.log_param("learning_rate", 1e-4)
    mlflow.log_param("batch_size", 10)
    mlflow.log_param("epochs", 180)

    # Fit the model and log metrics
    history = model.fit(
        x=x_train,
        y=y_train,
        batch_size=10,
        epochs=180,
        validation_data=(x_test, y_test),
    )

    # Save the model and log it as an artifact
    model.save("./models/license_plate_frame_recognition_model.keras")
    mlflow.log_artifact("./models/license_plate_frame_recognition_model.keras", artifact_path="models")

    # Log any additional custom metrics if needed
    final_train_loss = history.history["loss"][-1]
    final_val_loss = history.history["val_loss"][-1]
    mlflow.log_metric("final_train_loss", final_train_loss)
    mlflow.log_metric("final_val_loss", final_val_loss)


# Load model
# model = tf.keras.models.load_model('./models/license_plate_frame_recognition_model.keras')
# print('Model loaded Sucessfully')
