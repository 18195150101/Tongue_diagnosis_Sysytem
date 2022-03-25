import os
import json
import glob

import tensorflow as tf
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib import pylab

from esophagus_cancer_classification.esophagus_classification_model import resnet50


def main():
    im_height = 224
    im_width = 224
    num_classes = 2

    # load image
    for i in range(9):
        img_path = "user_test/" +str(i)+ ".jpg"
        assert os.path.exists(img_path), "file: '{}' dose not exist.".format(img_path)
        img = Image.open(img_path)
        #    resize image to 224x224
        img = img.resize((im_width, im_height))
        plt.imshow(img)

        # scaling pixel value to (0-1)
        _R_MEAN = 123.68
        _G_MEAN = 116.78
        _B_MEAN = 103.94
        img = np.array(img).astype(np.float32)
        img = img - [_R_MEAN, _G_MEAN, _B_MEAN]

        # Add the image to a batch where it's the only member.
        img = (np.expand_dims(img, 0))

        # read class_indict
        json_path = 'class_indices_esophagus.json'
        assert os.path.exists(json_path), "file: '{}' dose not exist.".format(json_path)
        json_file = open(json_path, "r")
        class_indict = json.load(json_file)

        feature = resnet50(num_classes=2, include_top=False)
        feature.trainable = False
        model = tf.keras.Sequential([feature,
                                     tf.keras.layers.GlobalAvgPool2D(),
                                     tf.keras.layers.Dropout(rate=0.5),
                                     tf.keras.layers.Dense(1024, activation="relu"),
                                     tf.keras.layers.Dropout(rate=0.5),
                                     tf.keras.layers.Dense(num_classes),
                                     tf.keras.layers.Softmax()])

        weights_path = './sample_weights/resNet_50.ckpt'
        assert len(glob.glob(weights_path + "*")), "cannot find {}".format(weights_path)
        model.load_weights(weights_path)
        # prediction
        result = np.squeeze(model.predict(img))
        predict_class = np.argmax(result)

        print_res = "class: {}   prob: {:.3}".format(class_indict[str(predict_class)],
                                                     result[predict_class])
        plt.title(print_res)
        print(print_res)
        plt.xticks([]), plt.yticks([])
        plt.show()



if __name__ == '__main__':
    main()
