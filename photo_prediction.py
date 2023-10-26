"""This code was being used to attempt to build a machine learning model that could detect the presence of mantas.
It is not currently accurate enough to replace manual searching"""

# def predictImage(model, img):
#     img_array = image.img_to_array(img)
#     img_array = np.expand_dims(img_array, axis=0)
#     img_array /= 255.0

#     predictions = model.predict(img_array)
#     predicted_class_index = np.argmax(predictions)

#     class_labels = ["empty", "fish"]
#     predicted_class_label = class_labels[predicted_class_index]

#     return predicted_class_label

# def predictAllImagesInDir(data, directory):
#     filesInDirectory = os.listdir(directory)
#     for fileName in filesInDirectory:
#         new_image_path = directory + fileName
#         img = image.load_img(new_image_path, target_size=(img_height, img_width))
#         predicted_class_label = predictImage(data.model, img)
#         print("File", fileName, "is predicted to be class:", predicted_class_label)
#         if predicted_class_label == "fish":
#             # try predicting now using original image of full qua;
#             data.fileNamesWithFish.append(new_image_path)
#             # manuallyAnalyseImage(data, new_image_path)

# def loadModel(data):
#     data.model = load_model('test_sketches/model.keras')