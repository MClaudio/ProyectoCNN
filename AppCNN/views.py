from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from AppCNN import models
from AppCNN.logica import modeloCNN
import numpy as np
from django.template import RequestContext


# Create your views here.

class Clacificacion():
    def formImagen(request):
        return render(request, "formImagen.html")

    def predecirImagen(request):
        image = models.Image()
        #print('Se carga la imagen')
        if request.method == 'POST' and request.FILES['myfile']:
            myfile = request.FILES['myfile']
            fs = FileSystemStorage()
            #filename = fs.save(myfile.name, myfile)
            #uploaded_file_url = fs.url(filename)
            name = fs.save(myfile.name, myfile)
            pathImg = fs.url(name)

            print(pathImg)
            #modeloCNN.modeloCNN.predecirImagen(modeloCNN, pathImg)

            nombreArchivoModelo = r'AppCNN/logica/arquitectura'
            nombreArchivoPesos = r'AppCNN/logica/pesos'

            Selectedmodel = modeloCNN.modeloCNN.cargarRNN(modeloCNN, nombreArchivoModelo, nombreArchivoPesos)
            pic = modeloCNN.modeloCNN.preImagen(modeloCNN, myfile)
            y_pred = modeloCNN.modeloCNN.predecirImagen(modeloCNN, pic, Selectedmodel)

            img = models.Image()
            img.image = name
            img.label = modeloCNN.modeloCNN.readLabels(modeloCNN, np.argmax(y_pred))
            img.probability = round(y_pred.max(), 2) * 100

            print('imagen: ', img.image)
            print('label: ',img.label)
            print('Probabilidad: ',img.probability)

            #print(resul.label)
            return render(request, "resultados.html", {"img":img})
        else:
            return redirect('/')


