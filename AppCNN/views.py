from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from AppCNN import models
from rest_framework import generics
from AppCNN.logica import modeloCNN
from AppCNN import serializers
import numpy as np
import pyrebase

import os




# Create your views here.
config = {

    'apiKey': "AIzaSyDBYpL2tb3yh3SIPo2BFhlS7slKruVGOic",
    'authDomain': "proyectotiendajpri.firebaseapp.com",
    'databaseURL': "https://proyectotiendajpri.firebaseio.com",
    'projectId': "proyectotiendajpri",
    'storageBucket': "proyectotiendajpri.appspot.com",
    'messagingSenderId': "1046831721926",
    'appId': "1:1046831721926:web:7402a636a8cd165f4b16c7",
    'measurementId': "G-MKSCN84RDE"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

class Autenticacion():

    def singIn(request):

        return render(request, "signIn.html")

    def postsign(request):
        email=request.POST.get('email')
        passw = request.POST.get("pass")
        try:
            user = auth.sign_in_with_email_and_password(email,passw)
        except:
            message = "invalid cerediantials"
            return render(request,"signIn.html",{"msg":message})
        print(user)
        return render(request, "welcome.html",{"e":email})

class ListImg(generics.ListCreateAPIView):
    queryset = models.Image.objects.all()
    serializer_class = serializers.ImageSerializer


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
            BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            img_dir= os.path.join(BASE_DIR, 'AppCNN/media/'+myfile.name)

            nombreArchivoModelo = r'AppCNN/logica/arquitectura'
            nombreArchivoPesos = r'AppCNN/logica/pesos'

            Selectedmodel = modeloCNN.modeloCNN.cargarRNN(modeloCNN, nombreArchivoModelo, nombreArchivoPesos)
            pic = modeloCNN.modeloCNN.preImagen(modeloCNN, img_dir)
            y_pred = modeloCNN.modeloCNN.predecirImagen(modeloCNN, pic, Selectedmodel)

            img = models.Image()
            img.image = myfile
            img.label = modeloCNN.modeloCNN.readLabels(modeloCNN, np.argmax(y_pred))
            img.probability = round((y_pred.max() * 100), 2)
            try:
                img.save()
            except:
                print('Error al guardar.')

            print('imagen: ', img.image)
            print('label: ',img.label)
            print('Probabilidad: ',img.probability)

            #print(resul.label)
            return render(request, "resultados.html", {"img":img})
        else:
            return redirect('/')


