import tensorflow as tf
import os


path_folder= os.getcwd()
print(path_folder)
path= os.path.join(path_folder, "Train/Character_Data")
print(path)

model = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(64, (3,3), activation='relu', padding= 'same', input_shape= (38,38,3)),
    tf.keras.layers.Conv2D(64, (3,3), activation='relu', padding= 'same'),
    tf.keras.layers.MaxPool2D(pool_size=(2,2), strides=(2,2)),
    
    tf.keras.layers.Conv2D(128, (3,3), activation='relu', padding= 'same'),
    tf.keras.layers.Conv2D(128, (3,3), activation='relu', padding= 'same'),
    tf.keras.layers.MaxPool2D(pool_size=(2,2)),

    tf.keras.layers.Conv2D(256, (3,3), activation='relu', padding= 'same'),
    tf.keras.layers.Conv2D(256, (3,3), activation='relu', padding= 'same'),
    tf.keras.layers.Conv2D(256, (3,3), activation='relu', padding= 'same'),
    tf.keras.layers.MaxPool2D(pool_size=(2,2), strides=(2,2)),

    tf.keras.layers.Conv2D(512, (3,3), activation='relu', padding= 'same'),
    tf.keras.layers.Conv2D(512, (3,3), activation='relu', padding= 'same'),
    tf.keras.layers.Conv2D(512, (3,3), activation='relu', padding= 'same'),
    tf.keras.layers.MaxPool2D(pool_size=(2,2), strides=(2,2)),

    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(512, activation= 'relu'),
    tf.keras.layers.Dense(512, activation= 'relu'),
    tf.keras.layers.Dense(31, activation= 'softmax')]) 

model.summary()

train_datagen= tf.keras.preprocessing.image.ImageDataGenerator(rescale = 1./255)
train_generator = train_datagen.flow_from_directory(path,
                                                   target_size= (38, 38),
                                                   batch_size= 32,
                                                   class_mode= 'categorical')

"""labels = (train_generator.class_indices)
print(labels)
print(len(labels))"""

model.compile(
    loss='categorical_crossentropy',
    optimizer=tf.keras.optimizers.Adam(0.001),
    metrics=['acc'],
)

history= model.fit(
    train_generator,
    steps_per_epoch=50,
    epochs=100)

model.save("my_model.h5")