from tensorflow.keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras import backend as kb
from PIL import Image
import os

img_width, img_height = 224, 224
#폴더 경로
train_data_dir = 'AImodelData/chest_xray/train'
test_data_dir = 'AImodelData/chest_xray/test'
#test, train 이미지 갯수 (steps per epoch 구하는데 사용)
num_train_samples = 530
num_test_samples = 74
epochs = 10 #약간 낮은 상태
batch_size = 16

#2가지 RGB 포맷 모두 사용 가능
if kb.image_data_format() == 'channels_first':
	input_shape = (3, img_width, img_height)
else:
	input_shape = (img_width, img_height, 3)

#모델
model = Sequential()
model.add(Conv2D(32, (2, 2), input_shape=input_shape))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(32, (2, 2), input_shape=input_shape))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Flatten())
model.add(Dense(64))
model.add(Activation('relu'))
model.add(Dropout(0.5))
model.add(Dense(1))
model.add(Activation('sigmoid'))

model.compile(loss='binary_crossentropy', #출력이 binary
			optimizer='rmsprop',
			metrics=['accuracy'])

train_data = ImageDataGenerator(
	rescale=1. / 255,
	shear_range=0.2,
	zoom_range=0.2,
	horizontal_flip=True)

test_data = ImageDataGenerator(rescale=1. / 255)

train_generator = train_data.flow_from_directory(
	train_data_dir,
	target_size=(img_width, img_height),
	batch_size=batch_size,
	class_mode='binary')

test_generator = test_data.flow_from_directory(
	test_data_dir,
	target_size=(img_width, img_height),
	batch_size=batch_size,
	class_mode='binary')

model.fit(
	train_generator,
	steps_per_epoch=num_train_samples // batch_size,
	epochs=epochs,
	validation_data=test_generator,
	validation_steps=num_test_samples // batch_size)

model.save('model.h5') #저장
