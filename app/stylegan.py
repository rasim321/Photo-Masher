import tensorflow as tf
import tensorflow_hub as hub
# Load compressed models from tensorflow_hub
CUDA_VISIBLE_DEVICES=""


# print(tf.__version__)
import numpy as np
import PIL

# content_path = "static/retrieved/2.JPEG"
# style_path = "static/style_images/1.JPEG"

def tensor_to_image(tensor):
    tensor = tensor*255
    tensor = np.array(tensor, dtype=np.uint8)
    if np.ndim(tensor)>3:
        assert tensor.shape[0] == 1
        tensor = tensor[0]
    return PIL.Image.fromarray(tensor)

def load_img(path_to_img):
    img = tf.io.read_file(path_to_img)
    img = tf.io.decode_image(img, channels=3)
    img = tf.image.convert_image_dtype(img, tf.float32)
    original_shape = img.shape #preserving the original shape of the content image
    img = tf.image.resize(img, (512, 512))
    img = img[tf.newaxis, :]

    return img, original_shape

# style_predict_path = tf.keras.utils.get_file('style_predict.tflite', 'https://tfhub.dev/google/lite-model/magenta/arbitrary-image-stylization-v1-256/int8/prediction/1?lite-format=tflite')
# style_transform_path = tf.keras.utils.get_file('style_transform.tflite', 'https://tfhub.dev/google/lite-model/magenta/arbitrary-image-stylization-v1-256/int8/transfer/1?lite-format=tflite')
def style_transfer(content_path, style_path):

    #We return the original shape to resize the composite image after processing
    content_image, original_shape = load_img(content_path)
    style_image, original_shape_style = load_img(style_path)

    hub_model = hub.load('https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2')
    stylized_image = hub_model(tf.constant(content_image), tf.constant(style_image))[0]
    return tensor_to_image(tf.image.resize(stylized_image, original_shape[0:2]))

# if __name__ == "__main__":
    # pic = style_transfer(content_path, style_path)
    # pic.save('static/composite.JPEG')
    # print("done")

    # print("working?")
    # composite_image = style_transfer('content.JPEG', 'style.JPEG')
    # composite_filepath = "comp_new.JPEG"
    # composite_image.save(composite_filepath)
