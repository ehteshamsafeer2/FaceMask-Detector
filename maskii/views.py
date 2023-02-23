from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import *
from .models import FileUpload

import numpy as np
import os
import shutil
import sys
from glob import glob
from keras.preprocessing import image
from tensorflow.keras.preprocessing import image
from keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPool2D
from tensorflow.keras.layers import Activation, Dropout, Flatten, Dense, Input
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from glob import glob
from tensorflow.keras.preprocessing import image
from tensorflow.keras.utils import plot_model

def mask_detect(request):
	if request.method == 'POST':
		form = DetectForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			return redirect('success')
	else:
		form = DetectForm()
	return render(request, 'index.html', {'form': form})

def success(request):
	CNN_aug_new = Sequential()
	CNN_aug_new.add(Input(shape=(75, 75, 3)))
	for n_filters in [16,32, 64]:
		CNN_aug_new.add(Conv2D(n_filters,strides=(2, 2), kernel_size=3, activation='relu'))
	CNN_aug_new.add(Flatten())
	CNN_aug_new.add(Dense(128, activation='relu'))
	CNN_aug_new.add(Dense(2, activation='softmax'))
	CNN_aug_new.compile(loss='categorical_crossentropy', metrics=['accuracy'], optimizer='adam')
	CNN_aug_new.load_weights('maskii\model_weights.h5')

	mydata = FileUpload.objects.last()
	path = str(mydata.img)
	print(path)
	img = image.load_img('media\\'+path,target_size=(75, 75))
	img = image.img_to_array(img)
	img = np.array([img])
	datagen = ImageDataGenerator(rescale=1/255)
	aug_iter = datagen.flow(img, batch_size=1)
	prediction=CNN_aug_new.predict(aug_iter)
	result = 'mask' if np.argmax(prediction)==0 else 'nomask'
	return render(request, 'result.html', {'res' : result})

