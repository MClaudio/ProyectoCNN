import pandas as pd
import numpy as np
from tensorflow.python.keras.models import load_model, model_from_json
from keras import backend as K
from tensorflow.python.keras.models import Sequential
from keras.preprocessing.image import array_to_img, img_to_array, load_img

from matplotlib import image
import cv2

class modeloCNN():

    Selectedmodel = Sequential()

    def cargarRNN(self, nombreArchivoModelo,nombreArchivoPesos):
        K.reset_uids()
        # Cargar la Arquitectura desde el archivo JSON
        with open(nombreArchivoModelo+'.json', 'r') as f:
            model = model_from_json(f.read())
        # Cargar Pesos (weights) en el nuevo modelo
        model.load_weights(nombreArchivoPesos+'.h5')
        #print("Red Neuronal Cargada desde Archivo")
        return model

    def preImagen(self, img):
        print('Imagen recibida',img)
        img_data = image.imread(img)
        img_data = cv2.resize(img_data, (100, 100))
        loaded_images = img_data
        mult_pxl = np.array(loaded_images)

        pic = mult_pxl.astype('float32')/255
        pic = pic.reshape(1, 100, 100, 3)
        print(pic.shape)
        return pic

    def readLabels(self, idx):
        df = pd.read_csv(r'AppCNN/logica/labels.csv', sep=';')
        return df['target_labels'][idx]

    def predecirImagen(self, pic, Selectedmodel):
        print('Red Neuronal')
        #nombreArchivoModelo =r'AppCNN/logica/arquitectura'
        #nombreArchivoPesos =r'AppCNN/logica/pesos'
        #self.Selectedmodel = self.cargarRNN(self, nombreArchivoModelo, nombreArchivoPesos)
        #print(self.Selectedmodel)
        #mult_pxl, mult_label = self.cargaImagen(dir_path)
        y_pred = Selectedmodel.predict(pic)
        #pred_idx = np.argmax(y_pred)

        return y_pred

#https://simpleisbetterthancomplex.com/tutorial/2016/08/01/how-to-upload-files-with-django.html