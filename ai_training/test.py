import tensorflow as tf 
import argparse
import numpy as np
import matplotlib.pylab as plt

def main(args):
    """
    Prints the overall classification accuracy of the model as well as the the instances 
    when the image was wrongly classified.
    """    
    img_shape = (224, 224)
    batch_size = 32

    datagen = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1./255)
    dataset = datagen.flow_from_directory(
        args.dataset_path,
        shuffle=True,
        target_size=img_shape,
        batch_size=batch_size
    )
    
    labels = load_labels(args.labels_file)
    interpreter = tf.lite.Interpreter(args.model_file)

    error_count = 0
    for _ in range(dataset.samples):
        interpreter.allocate_tensors()
        _, height, width, _ = interpreter.get_input_details()[0]['shape']
        x, y = next(dataset)
        image = x[0, :, :, :]
        true_index = np.argmax(y[0])

        top_k = 1
        set_input_tensor(interpreter, image)
        interpreter.invoke()
        output_details = interpreter.get_output_details()[0]
        output = np.squeeze(interpreter.get_tensor(output_details['index']))
        ordered = np.argpartition(-output, top_k)
        results = [(i, output[i]) for i in ordered[:top_k]]
        label_id, prob = results[0]

        if labels[true_index] != labels[label_id]:
            plt.imshow(image)
            plt.axis('off')
            plt.title('Error number ' + str(error_count))
            plt.show()
            print("\n Wrong guess, Error number " + str(error_count) + "\n True label: " + labels[true_index] + " Probability: " + str(prob))
            print("Predicted label: " + labels[label_id])
            error_count += 1
    print('Validation accuracy is {}'.format((1.0 - (error_count / dataset.samples)) * 100.0))

def set_input_tensor(interpreter, image):
  tensor_index = interpreter.get_input_details()[0]['index']
  input_tensor = interpreter.tensor(tensor_index)()[0]
  input_tensor[:, :] = image

def load_labels(path):
    """Loads the file path of the labels file."""
    with open(path, 'r') as f:
        return {i: line.strip() for i, line in enumerate(f.readlines())}
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--labels_file',
        type=str,
        help='file name containing the labels')
    parser.add_argument(
        '--model_file',
        type=str,
        help='file name containing the tflite model')
    parser.add_argument(
        '--dataset_path', 
        type=str,
        help='path to the dataset containing the images')
    args = parser.parse_args()
    
    main(args)

