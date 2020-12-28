import tensorflow as tf
import picamera
import PIL.Image
import numpy as np
import argparse
import time
from motor import Motor

def classify(args, labels, interpreter, lamp):
    """
    Takes the image of the object and returns its name ('plastic', 'metal', 'carton') and the probability of it. 
    If there is no object, returns 'None'.
    """    
    # Setting up the model and the labels

    lamp.forward(100)
    interpreter.allocate_tensors()
    _, height, width, _ = interpreter.get_input_details()[0]['shape']
    
    # Opening camera and capturing the image
    with picamera.PiCamera() as camera:
        # Capture and resize the image
        time.sleep(.2)
        camera.resolution(1280, 720)
        
        # This detected.jpg will always override in every recycle, so do not worry about memory issues.
        camera.capture('detected.jpg')
        image = PIL.Image.open('detected.jpg').convert('RGB').resize((width, height),
                                                         PIL.Image.ANTIALIAS)
        # Classify the image
        lamp.stop()
        results = classify_image(interpreter, image)
        label_id, prob = results[0]
        
        if prob >= args.min_prob:
            return labels[label_id]
        return None

def set_input_tensor(interpreter, image):
  tensor_index = interpreter.get_input_details()[0]['index']
  input_tensor = interpreter.tensor(tensor_index)()[0]
  input_tensor[:, :] = image

def classify_image(interpreter, image, top_k=1):
  """Returns a sorted array of classification results."""
  set_input_tensor(interpreter, image)
  interpreter.invoke()
  output_details = interpreter.get_output_details()[0]
  output = np.squeeze(interpreter.get_tensor(output_details['index']))

  # If the model is quantized (uint8 data), then dequantize the results
  if output_details['dtype'] == np.uint8:
    scale, zero_point = output_details['quantization']
    output = scale * (output - zero_point)

  ordered = np.argpartition(-output, top_k)
  return [(i, output[i]) for i in ordered[:top_k]]

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
        '--lamp_pins', 
        nargs='+',
        type=int,
        help='pins of the lamp')
    args = parser.parse_args()
    
    labels = load_labels(args.labels_file)
    interpreter = tf.lite.Interpreter(args.model_file)

    lamp = Motor(args.lamp_pins)
    lamp.forward(100)
    lamp.stop()
    
    classify(args, labels, interpreter, lamp)
