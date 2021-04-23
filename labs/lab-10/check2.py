# TensorFlow and tf.keras
import tensorflow as tf

# Helper libraries
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageOps

print(tf.__version__)

fashion_mnist = tf.keras.datasets.fashion_mnist

(train_X, train_y), (test_X,test_y) = fashion_mnist.load_data()

class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

print(train_X.shape, train_y.shape)
print(test_X.shape, test_y.shape)

plt.figure()
plt.imshow(train_X[0])
plt.colorbar()
plt.grid(False)
plt.show()

train_X = train_X / 255.0
test_X = test_X / 255.0

plt.figure(figsize=(10,10))
for i in range(25):
    plt.subplot(5,5,i+1)
    plt.xticks([])
    plt.yticks([])
    plt.grid(False)
    plt.imshow(train_X[i], cmap=plt.cm.binary)
    plt.xlabel(class_names[train_y[i]])
plt.show()

# normally you'd use a Conv2D layer in the beginning...
model = tf.keras.Sequential([
    tf.keras.layers.Flatten(input_shape=(28, 28)),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(10),
    tf.keras.layers.Softmax()])

# you could probably just use normal categorical cross
model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

model.fit(train_X, train_y, epochs=10)

test_loss, test_acc = model.evaluate(test_X, test_y, verbose=2)
print('\nTest accuracy:', test_acc)

preds = model.predict(test_X)

def plot_image(i, predictions_array, true_label, img):
  true_label, img = true_label[i], img[i]
  plt.grid(False)
  plt.xticks([])
  plt.yticks([])

  plt.imshow(img, cmap=plt.cm.binary)

  predicted_label = np.argmax(predictions_array)
  if predicted_label == true_label:
    color = 'blue'
  else:
    color = 'red'

  plt.xlabel("{} {:2.0f}% ({})".format(class_names[predicted_label],
                                100*np.max(predictions_array),
                                class_names[true_label]),
                                color=color)

def plot_value_array(i, predictions_array, true_label):
  true_label = true_label[i]
  plt.grid(False)
  plt.xticks(range(10))
  plt.yticks([])
  thisplot = plt.bar(range(10), predictions_array, color="#777777")
  plt.ylim([0, 1])
  predicted_label = np.argmax(predictions_array)

  thisplot[predicted_label].set_color('red')
  thisplot[true_label].set_color('blue')

# Plot the first X test images, their predicted labels, and the true labels.
# Color correct predictions in blue and incorrect predictions in red.
print('Checkpoint 2')
num_rows = 5
num_cols = 3
num_images = num_rows*num_cols
offset = 9000
plt.figure(figsize=(2*2*num_cols, 2*num_rows))
for i in range(num_images):
  plt.subplot(num_rows, 2*num_cols, 2*i+1)
  plot_image(i+offset, preds[i+offset], test_y, test_X)
  plt.subplot(num_rows, 2*num_cols, 2*i+2)
  plot_value_array(i+offset, preds[i+offset], test_y)
plt.tight_layout()
plt.show()

imgs = ['ankleboots.png', 'sneakers.jpg', 'trousers.jpg']

# open, display, and predict an image
def predStr(name):
    img = Image.open(name)
    # convert to greyscale
    img = img.resize((28, 28))
    img = img.convert('RGB')
    img = ImageOps.invert(img)
    img = ImageOps.grayscale(img)
    img.save(name[:-4] + '_converted' + name[-4:])
    img_arr = np.array(img)
    img_arr = img_arr / 255.0
    # predict and show the name
    prediction = model.predict(np.array([img_arr]))
    return class_names[np.argmax(prediction)]

print('Checkpoint 3')
for img in imgs:
    # print class type
    print(img[:-4])
    # print out predicted type
    print(predStr(img))