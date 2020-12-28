import tensorflow as tf 
import tensorflow_hub as hub
import argparse
import numpy
import datetime

def main(args):
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

    classifier_model = "https://tfhub.dev/google/imagenet/mobilenet_v2_100_224/feature_vector/4"
    datagen_kwargs = dict(rescale=1./255, rotation_range=30, brightness_range=(0.5, 1.0), vertical_flip=True, horizontal_flip=True, validation_split=0.2) # Pre-processing methods
    img_shape = (224, 224)

    train_datagen = tf.keras.preprocessing.image.ImageDataGenerator(**datagen_kwargs)
    train_data = train_datagen.flow_from_directory(
        args.data_root,
        shuffle=True,
        target_size=img_shape,
        batch_size=args.batch_size,
        subset='training'
    )
    valid_data = train_datagen.flow_from_directory(
        args.data_root,
        shuffle=True,
        target_size=img_shape,
        batch_size=args.batch_size,
        subset='validation'
    )

    model = tf.keras.Sequential([
        # Explicitly define the input shape so the model can be properly
        # loaded by the TFLiteConverter
        tf.keras.layers.InputLayer(input_shape=img_shape+(3,)),
        hub.KerasLayer(classifier_model, trainable=args.do_finetuning),
        tf.keras.layers.Dropout(rate=0.5),
        tf.keras.layers.Dense(train_data.num_classes, activation='softmax')
    ])
    model.build((None,)+img_shape+(3,))
    if args.checkpoint_path != None:
        model.load_weights(args.checkpoint_path)

    model.compile(optimizer=tf.keras.optimizers.Adam(args.lr),
            loss=tf.keras.losses.CategoricalCrossentropy(from_logits=True),
            metrics=['acc'])
    model.summary()
    
    steps_per_epoch = train_data.samples // train_data.batch_size
    validation_steps = valid_data.samples // valid_data.batch_size
    
    # Dont forget to clear out prior loggin data by "!rm -rf logs/image"
    logdir = "logs/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    
    # Define the basic TensorBoard callback.ab
    tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=logdir)
    cp_callback = tf.keras.callbacks.ModelCheckpoint(
            filepath="checkpoints/cp-{epoch:04d}.ckpt", 
            verbose=1, 
            save_weights_only=True,
            save_freq=args.checkpoint_freq*args.batch_size)
    
    history = model.fit(train_data, epochs=args.epoch,
            steps_per_epoch=steps_per_epoch,
            validation_data=valid_data,
            validation_steps=validation_steps,
            callbacks=[tensorboard_callback, cp_callback])

    # To see the logs after training, use "%tensorboard --logdir logs/image"

    # Converting model into TensorflowLite model
    saved_model_dir = args.save_dir # '[directory you want to save your model to]'
    tf.saved_model.save(model, saved_model_dir)

    converter = tf.lite.TFLiteConverter.from_saved_model(saved_model_dir)
    tflite_model = converter.convert()

    # Saving the model and label map into two seperate files for further use
    with open('model.tflite', 'wb') as f:
        f.write(tflite_model)

    labels = '\n'.join(sorted(train_data.class_indices.keys()))

    with open('labels.txt', 'w') as f:
        f.write(labels)
        
    # All that is left is to use this TFLite model in your Raspberry Pi 4.
                    
if __name__ == "__main__":
    # Arguments
    parser = argparse.ArgumentParser()
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
    parser.add_argument(
        '--lr',
        type=float,
        default=0.001,
        help='learning rate')
    parser.add_argument(
        '--data_root',
        type=str,
        help='path to your dataset')
    parser.add_argument(
        '--save_dir',
        type=str,
        help='directory to save your tflite model and your checkpoints')
    parser.add_argument(
        '--do_finetuning',
        type=bool,
        default=True,
        help='fine tuning?')
    parser.add_argument(
        '--checkpoint_path',
        type=str,
        default=None,
        help='path to your checkpoint file')
    parser.add_argument(
        '--checkpoint_freq',
        type=int,
        default=5,
        help='How frequent (in terms of epoch) is checkpoint saved')

    args = parser.parse_args()
    main(args)