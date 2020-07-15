import tensorflow as tf
import keras_preprocessing
from keras_preprocessing.image import ImageDataGenerator

TRAINING_DIR = "../dataset"
training_datagen = ImageDataGenerator(
    rescale = 1./255,
    rotation_range=50,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest',
    validation_split=0.15)


train_generator = training_datagen.flow_from_directory(
    TRAINING_DIR,
    target_size=(120, 120),
    class_mode='categorical',
    batch_size=16,
    subset='training'
)

validation_generator = training_datagen.flow_from_directory(
    TRAINING_DIR,
    target_size=(120, 120),
    class_mode='categorical',
    batch_size=16,
    subset='validation'
)

model = tf.keras.models.Sequential([
    # This is the first convolution
    tf.keras.layers.Conv2D(64, (3,3), activation='relu', input_shape=(120, 120, 3)),
    tf.keras.layers.MaxPooling2D(2, 2),
    tf.keras.layers.Dropout(0.2),
    # The second convolution
    tf.keras.layers.Conv2D(64, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Dropout(0.2),
    # The third convolution
    tf.keras.layers.Conv2D(128, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Dropout(0.2),
    # The fourth convolution
    tf.keras.layers.Conv2D(128, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Dropout(0.2),
    # Flatten the results to feed into a DNN
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dropout(0.2),
    # 512 neuron hidden layer
    tf.keras.layers.Dense(512, activation='relu'),
    tf.keras.layers.Dense(4, activation='softmax')
])

model.summary()

lr = tf.keras.optimizers.schedules.ExponentialDecay(1e-3, train_generator.samples // 16, 0.95)

model.compile(loss = 'categorical_crossentropy', optimizer=tf.keras.optimizers.Adam(learning_rate=lr), metrics=['accuracy'])

callbacks = [
    tf.keras.callbacks.EarlyStopping(monitor='val_loss', min_delta=0, patience=14),
    tf.keras.callbacks.ModelCheckpoint("cycle_classifier_proto_2.h5", monitor='val_accuracy', save_best_only=True)
]

history = model.fit_generator(
    train_generator,
    epochs=60,
    steps_per_epoch=train_generator.samples // 16,
    validation_data=validation_generator, 
    validation_steps=validation_generator.samples // 16,
    callbacks=callbacks,
)

converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()
open("model.tflite", "wb").write(tflite_model)