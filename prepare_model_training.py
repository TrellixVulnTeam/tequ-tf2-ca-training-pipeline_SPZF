import os
import json
import io
import random
import PIL.Image
import tensorflow as tf
import tarfile
import sys
import six.moves.urllib as urllib
from object_detection.utils import dataset_util
from object_detection.utils import label_map_util
import re
from google.protobuf import text_format
from object_detection.utils import config_util
from object_detection.utils import label_map_util

basepath = os.getcwd()

#Base model
#NUM_TRAIN_STEPS  = int(input("Set number of training steps: ").strip())
TRAIN_CONFIG_BATCH_SIZE = int(input("Set batch size: ").strip())
TRAIN_FILES_PERCENT = 0.7


print("\r\n\r\n")
print("Available base models:\r\n")
print("1 - ssd_mobilenet_v2_fpnlite_320x320_coco17_tpu-8\n")
print("2 - ssd_mobilenet_v2_320x320_coco17_tpu-8\n")
print("\r\n\r\n")

model_selection = int(input("Select base model: ").strip())

if model_selection == 1:
	MODEL_TYPE = 'ssd_mobilenet_v2_fpnlite_320x320_coco17_tpu-8'
	CONFIG_TYPE = 'ssd_mobilenet_v2_fpnlite_320x320_coco17_tpu-8'
elif model_selection == 2:
	MODEL_TYPE = 'ssd_mobilenet_v2_320x320_coco17_tpu-8'
	CONFIG_TYPE = 'ssd_mobilenet_v2_320x320_coco17_tpu-8'
else:
	print("*** Unknown model selected!")
	exit()


#print("Number of training steps: %d" % NUM_TRAIN_STEPS)
print("\r\n\r\n")
print("*** Batch size: %d" % TRAIN_CONFIG_BATCH_SIZE)
print("*** Base model %s selected" % MODEL_TYPE)

f = open("batch_size.txt", "w")
f.write(str(TRAIN_CONFIG_BATCH_SIZE))
f.close()

f = open("base_model.txt", "w")
f.write(str(model_selection))
f.close()

f = open("model_type.txt", "w")
f.write(str(MODEL_TYPE))
f.close()

f = open("train_files_percent.txt", "w")
f.write(str(TRAIN_FILES_PERCENT))
f.close()


CLOUD_ANNOTATIONS_MOUNT = sys.argv[1]
ANNOTATIONS_JSON_PATH   = sys.argv[2]
CHECKPOINT_PATH = sys.argv[3]
OUTPUT_PATH     = sys.argv[4]
EXPORTED_PATH   = sys.argv[5]
DATA_PATH       = sys.argv[6]
LABEL_MAP_PATH    = sys.argv[7]
TRAIN_RECORD_PATH = sys.argv[8]
VAL_RECORD_PATH   = sys.argv[9]
CONFIG_PATH       = sys.argv[10]

download_base = 'http://download.tensorflow.org/models/object_detection/tf2/20200711/'
model = MODEL_TYPE + '.tar.gz'
tmp = basepath+'\\content\\checkpoint.tar.gz'
print("*** Download link for selected base model: %s%s" % (download_base,model))
print("\r\n\r\n")

#Functions
def create_tf_record(images, annotations, label_map, image_path, output):
  # Create a train.record TFRecord file.
  with tf.io.TFRecordWriter(output) as writer:
    # Loop through all the training examples.
    for image_name in images:
      try:
        # Make sure the image is actually a file
        img_path = os.path.join(image_path, image_name)   
        if not os.path.isfile(img_path):
          continue
          
        # Read in the image.
        with tf.io.gfile.GFile(img_path, 'rb') as fid:
          encoded_jpg = fid.read()

        # Open the image with PIL so we can check that it's a jpeg and get the image
        # dimensions.
        encoded_jpg_io = io.BytesIO(encoded_jpg)
        image = PIL.Image.open(encoded_jpg_io)
        if image.format != 'JPEG':
          raise ValueError('Image format not JPEG')

        width, height = image.size

        # Initialize all the arrays.
        xmins = []
        xmaxs = []
        ymins = []
        ymaxs = []
        classes_text = []
        classes = []

        # The class text is the label name and the class is the id. If there are 3
        # cats in the image and 1 dog, it may look something like this:
        # classes_text = ['Cat', 'Cat', 'Dog', 'Cat']
        # classes      = [  1  ,   1  ,   2  ,   1  ]

        # For each image, loop through all the annotations and append their values.
        for a in annotations[image_name]:
          if ("x" in a and "x2" in a and "y" in a and "y2" in a):
            label = a['label']
            xmins.append(a["x"])
            xmaxs.append(a["x2"])
            ymins.append(a["y"])
            ymaxs.append(a["y2"])
            classes_text.append(label.encode("utf8"))
            classes.append(label_map[label])
       
        # Create the TFExample.
        tf_example = tf.train.Example(features=tf.train.Features(feature={
          'image/height': dataset_util.int64_feature(height),
          'image/width': dataset_util.int64_feature(width),
          'image/filename': dataset_util.bytes_feature(image_name.encode('utf8')),
          'image/source_id': dataset_util.bytes_feature(image_name.encode('utf8')),
          'image/encoded': dataset_util.bytes_feature(encoded_jpg),
          'image/format': dataset_util.bytes_feature('jpeg'.encode('utf8')),
          'image/object/bbox/xmin': dataset_util.float_list_feature(xmins),
          'image/object/bbox/xmax': dataset_util.float_list_feature(xmaxs),
          'image/object/bbox/ymin': dataset_util.float_list_feature(ymins),
          'image/object/bbox/ymax': dataset_util.float_list_feature(ymaxs),
          'image/object/class/text': dataset_util.bytes_list_feature(classes_text),
          'image/object/class/label': dataset_util.int64_list_feature(classes),
        }))
        if tf_example:
          # Write the TFExample to the TFRecord.
          writer.write(tf_example.SerializeToString())
      except ValueError:
        print('Invalid example, ignoring.')
        pass
      except IOError:
        print("Can't read example, ignoring.")
        pass
  # Create a train.record TFRecord file.
  with tf.io.TFRecordWriter(output) as writer:
    # Loop through all the training examples.
    for image_name in images:
      try:
        # Make sure the image is actually a file
        img_path = os.path.join(image_path, image_name)   
        if not os.path.isfile(img_path):
          continue
          
        # Read in the image.
        with tf.io.gfile.GFile(img_path, 'rb') as fid:
          encoded_jpg = fid.read()

        # Open the image with PIL so we can check that it's a jpeg and get the image
        # dimensions.
        encoded_jpg_io = io.BytesIO(encoded_jpg)
        image = PIL.Image.open(encoded_jpg_io)
        if image.format != 'JPEG':
          raise ValueError('Image format not JPEG')

        width, height = image.size

        # Initialize all the arrays.
        xmins = []
        xmaxs = []
        ymins = []
        ymaxs = []
        classes_text = []
        classes = []

        # The class text is the label name and the class is the id. If there are 3
        # cats in the image and 1 dog, it may look something like this:
        # classes_text = ['Cat', 'Cat', 'Dog', 'Cat']
        # classes      = [  1  ,   1  ,   2  ,   1  ]

        # For each image, loop through all the annotations and append their values.
        for a in annotations[image_name]:
          if ("x" in a and "x2" in a and "y" in a and "y2" in a):
            label = a['label']
            xmins.append(a["x"])
            xmaxs.append(a["x2"])
            ymins.append(a["y"])
            ymaxs.append(a["y2"])
            classes_text.append(label.encode("utf8"))
            classes.append(label_map[label])
       
        # Create the TFExample.
        tf_example = tf.train.Example(features=tf.train.Features(feature={
          'image/height': dataset_util.int64_feature(height),
          'image/width': dataset_util.int64_feature(width),
          'image/filename': dataset_util.bytes_feature(image_name.encode('utf8')),
          'image/source_id': dataset_util.bytes_feature(image_name.encode('utf8')),
          'image/encoded': dataset_util.bytes_feature(encoded_jpg),
          'image/format': dataset_util.bytes_feature('jpeg'.encode('utf8')),
          'image/object/bbox/xmin': dataset_util.float_list_feature(xmins),
          'image/object/bbox/xmax': dataset_util.float_list_feature(xmaxs),
          'image/object/bbox/ymin': dataset_util.float_list_feature(ymins),
          'image/object/bbox/ymax': dataset_util.float_list_feature(ymaxs),
          'image/object/class/text': dataset_util.bytes_list_feature(classes_text),
          'image/object/class/label': dataset_util.int64_list_feature(classes),
        }))
        if tf_example:
          # Write the TFExample to the TFRecord.
          writer.write(tf_example.SerializeToString())
      except ValueError:
        print('Invalid example, ignoring.')
        pass
      except IOError:
        print("Can't read example, ignoring.")
        pass



# Get a list of labels from the annotations.json
labels = {}
with open(ANNOTATIONS_JSON_PATH) as f:
  annotations = json.load(f)
  labels = annotations['labels']
  print("Labels:", labels)

# Create a file named label_map.pbtxt
os.makedirs(DATA_PATH, exist_ok=True)
with open(LABEL_MAP_PATH, 'w') as f:
  # Loop through all of the labels and write each label to the file with an id
  for idx, label in enumerate(labels):
    f.write('item {\n')
    f.write("\tname: '{}'\n".format(label))
    f.write('\tid: {}\n'.format(idx + 1)) # indexes must start at 1
    f.write('}\n')
	
#Generate TFRecords
with open(ANNOTATIONS_JSON_PATH) as f:
  annotations = json.load(f)['annotations']
  image_files = [image for image in annotations.keys()]
  # Load the label map we created.
  label_map = label_map_util.get_label_map_dict(LABEL_MAP_PATH)

  random.seed(42)
  random.shuffle(image_files)
  num_train = int(TRAIN_FILES_PERCENT * len(image_files))
  train_examples = image_files[:num_train]
  val_examples = image_files[num_train:]

  create_tf_record(train_examples, annotations, label_map, CLOUD_ANNOTATIONS_MOUNT, TRAIN_RECORD_PATH)
  create_tf_record(val_examples, annotations, label_map, CLOUD_ANNOTATIONS_MOUNT, VAL_RECORD_PATH)

#Download a base model
if not (os.path.exists(CHECKPOINT_PATH)):
  # Download the checkpoint
  opener = urllib.request.URLopener()
  opener.retrieve(download_base + model, tmp)

  # Extract all the `model.ckpt` files.
  with tarfile.open(tmp) as tar:
      tar.extractall(path=CHECKPOINT_PATH)
      
  os.remove(tmp)
 
 
#Model config settings
pipeline_skeleton = CONFIG_PATH + CONFIG_TYPE + '.config'
configs = config_util.get_configs_from_pipeline_file(pipeline_skeleton)

label_map = label_map_util.get_label_map_dict(LABEL_MAP_PATH)
num_classes = len(label_map.keys())
meta_arch = configs["model"].WhichOneof("model")

override_dict = {
  'model.{}.num_classes'.format(meta_arch): num_classes,
  'train_config.batch_size': TRAIN_CONFIG_BATCH_SIZE,
  'train_input_path': TRAIN_RECORD_PATH,
  'eval_input_path': VAL_RECORD_PATH,
  'train_config.fine_tune_checkpoint': os.path.join(CHECKPOINT_PATH+'\\'+MODEL_TYPE+'\\checkpoint\\', 'ckpt-0'),
  'train_config.fine_tune_checkpoint_type': "detection",
  'label_map_path': LABEL_MAP_PATH
}

#Configure model
configs = config_util.merge_external_params_with_configs(configs, kwargs_dict=override_dict)
pipeline_config = config_util.create_pipeline_proto_from_configs(configs)
config_util.save_pipeline_config(pipeline_config, DATA_PATH)

print(override_dict)
