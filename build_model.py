"""This code was being used to attempt to build a machine learning model that could detect the presence of mantas.
It is not currently accurate enough to replace manual searching"""

# import os
# import tensorflow as tf
# from tensorflow.keras.preprocessing.image import ImageDataGenerator

# # Define data directories and parameters
# data_dir = "test_sketches"
# batch_size = 32
# img_height = 150
# img_width = 150

# # Create a data generator
# train_data_gen = ImageDataGenerator(
#     rescale=1.0/255.0,  # Normalize pixel values
#     validation_split=0.25  # Split data into training and validation sets
# )

# # Load and preprocess the training data
# train_generator = train_data_gen.flow_from_directory(
#     data_dir,
#     target_size=(img_height, img_width),
#     batch_size=batch_size,
#     class_mode='categorical',  # For multiple classes
#     subset='training'  # Use training subset
# )

# # Load and preprocess the validation data
# validation_generator = train_data_gen.flow_from_directory(
#     data_dir,
#     target_size=(img_height, img_width),
#     batch_size=batch_size,
#     class_mode='categorical',
#     subset='validation'  # Use validation subset
# )

# from tensorflow.keras.models import Sequential
# from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout

# # Define the CNN model
# model = Sequential([
#     Conv2D(32, (3, 3), activation='relu', input_shape=(img_height, img_width, 3)),
#     MaxPooling2D(2, 2),
#     Conv2D(64, (3, 3), activation='relu'),
#     MaxPooling2D(2, 2),
#     Conv2D(128, (3, 3), activation='relu'),
#     MaxPooling2D(2, 2),
#     Flatten(),
#     Dense(128, activation='relu'),
#     Dropout(0.5),
#     Dense(2, activation='softmax')  # 2 classes: "empty" and "fish"
# ])

# # Compile the model
# model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# # Train the model
# num_epochs = 40
# history = model.fit(train_generator, epochs=num_epochs, validation_data=validation_generator)

# # save model
# model.save('test_sketches/model_2.keras')