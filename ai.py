import tensorflow as tf 
import argparse
import numpy
import datetime

def main():
    classifier_model ="https://tfhub.dev/google/tf2-preview/mobilenet_v2/classification/4"

    #
    # The following data retrieval code is designed for data settings such as:
    #
    # Data Folder
    #    --> Training Image Folder/Validation Image Folder  (recommended split is 20% val, 80% training)
    #        --> class_1
    #        --> class_2
    #        --> class_3
    #        ...
    #    
    # The classes in this code are (metal, plastic, carton). You can add our delete any classes you like.
    #

    train_data_root = '/content/drive/My Drive/Dataset/train' # '[your data path in your computer or Google Colab]'
    val_data_root = '/content/drive/My Drive/Dataset/val' # '[your data path in your computer or Google Colab]'
    datagen_kwargs = dict(rescale=1./255, shear_range=0.2, zoom_range=0.2, horizontal_flip=True) # Pre-processing methods

    valid_datagen = tf.keras.preprocessing.image.ImageDataGenerator(**datagen_kwargs)
    valid_data = valid_datagen.flow_from_directory(
        train_data_root,
        shuffle=True,
        target_size=args.img_shape,
        batch_size=args.batch_size
    )
    train_datagen = tf.keras.preprocessing.image.ImageDataGenerator(**datagen_kwargs)
    train_data = train_datagen.flow_from_directory(
        val_data_root,
        shuffle=True,
        target_size=args.img_shape,
        batch_size=args.batch_size
    )

    # Pre-trained model from Tensorflow Hub    
    basemodel = tf.keras.Sequential([
       tf.hub.KerasLayer(classifier_model, input_shape=args.img_shape)
    ])

    model = tf.keras.Sequential([
        basemodel,
        tf.keras.layers.GlobalAveragePooling2D(),
        tf.keras.layers.Dense(args.num_classes, activation='softmax')
    ])

    model.compile(optimizer=tf.keras.optimizers.Adam(lr=args.lr),
            loss=tf.keras.losses.CategoricalCrossentropy(from_logits=True),
            metrics=['acc'])

    steps_per_epoch = numpy.ceil(len(train_data) / args.batch_size)
    validation_steps = numpy.ceil(len(valid_data) / args.batch_size)

    # Dont forget to clear out prior loggin data by "!rm -rf logs/image"
    logdir = "logs/image/" + datetime.now().strftime("%Y%m%d-%H%M%S")
    
    # Define the basic TensorBoard callback.
    tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=logdir)

    history = model.fit(train_data, epochs=args.epoch,
            steps_per_epoch=steps_per_epoch,
            validation_data=valid_data,
            validation_steps=validation_steps,
            callbacks=[tensorboard_callback])

    # To see the logs after training, use "%tensorboard --logdir logs/image"

    # Converting model into TensorflowLite model
    saved_model_dir = '/content/TFLite' # '[directory you want to save your model to]'
    tf.saved_model.save(model, saved_model_dir)

    converter = tf.lite.TFLiteConverter.from_saved_model(saved_model_dir)
    tflite_model = converter.convert()

    # Saving the model and label map into two seperate files for further use
    with open('model.tflite', 'wb') as f:
        f.write(tflite_model)

    labels = '\n'.join(sorted(train_data.class_indices.keys()))

    with open('labels.txt', 'w') as f:
        f.write(labels)

    #
    # All that is left is to use this TFLite model in your Raspberry Pi 4. 
    # Seeing how to implement it into Raspberry Pi 4, refer to "gui.py" and "functions.py".
    #

                    
if __name__ == "__main__":
    # Arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--img_shape', 
        type=tuple,
        default=(224, 224, 3),
        help='pins to which motor 1 is binded to')
    parser.add_argument(
        '--num_classes',
        type=int,
        default=6,
        help='number of classes')
    parser.add_argument(
        '--batch_size',
        type=int,
        default=32,
        help='batch size of the data')
    parser.add_argument(
        '--epoch',
        type=int,
        default=50,
        help='number of classes')

    args = parser.parse_args()