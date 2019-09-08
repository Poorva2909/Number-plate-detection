import os
import numpy as np
from sklearn.svm import SVC
from sklearn.model_selection import cross_val_score
from sklearn.externals import joblib
from skimage.io import imread
from skimage.filters import threshold_otsu

letters = [
             'A', 'B', 'C', 'D','E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P',
             'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
             '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'
        ]
print('Starting to read data:-- ')
def read_training_data(training_directory):
    img_info = []
    dest_info = []
    for every_let in letters:
        for each in range(10):
            image_path = os.path.join(training_directory, every_let, every_let + '_' + str(each) + '.jpg')
            # It is reading each image of each character in the given input data file
            img_details = imread(image_path, as_gray=True)
            binary_image = img_details < threshold_otsu(img_details)
            # the 2D array of each image is made flat because the ML classifier requires that each sample has to be in 1D array
            flat_bin_image = binary_image.reshape(-1)
            img_info.append(flat_bin_image)
            dest_info.append(every_let)

    return (np.array(img_info), np.array(dest_info))
print('image flattened')

print('Cross validation starts:-- ')
def cross_validation(model, num_of_fold, train_data, train_label):
    # this uses the concept of cross validation to measure the accuracy of a model,
    # Here, the num_of_fold determines the type of validation
    # e.g if num_of_fold is 6, then we are performing a 6-fold cross validation
    accuracy_result = cross_val_score(model, train_data, train_label,
                                      cv=num_of_fold)
    print("Cross Validation Result for ", str(num_of_fold), " -fold")

    print(accuracy_result * 100)
print('the reading data: ')
training_dataset_dir = 'C:/Users/admin/Documents/LicensePlateDetector-master/train20X20'
img_info, dest_info = read_training_data(training_dataset_dir)
print('Reading data has been completed')
print('')

# the kernel can be 'linear', 'poly' or 'rbf', the probability was set to True only
#to display the accuracy of model.
svc_model = SVC(kernel='linear', probability=True)

cross_validation(svc_model, 4, img_info, target_data)

print('the model for training')
print('start to train model by the input data')

# we will now train the model with all the input data that we have given

svc_model.fit(img_info, dest_info)

#next time the trained model will use the saved pattern for future prediction

import pickle
print("model has been trained, the training model:- ")
filename = 'C:/Users/admin/Documents/LicensePlateDetector-master/finalized_model.sav'
pickle.dump(svc_model, open(filename, 'wb'))
print("model has been saved for future predictions")
