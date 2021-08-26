import json
import os
import sys
from object_detection.utils.label_map_util import get_label_map_dict

basepath = os.getcwd()
labels_path = sys.argv[1]
MODEL_TYPE = sys.argv[2]
TRAIN_BATCH_SIZE = sys.argv[3]
TRAIN_FILES_PERCENT = sys.argv[4]
NUM_TRAIN_STEPS = sys.argv[5]

DATA_PATH       = basepath+'\\content\\data'
LABEL_MAP_PATH    = os.path.join(DATA_PATH, 'label_map.pbtxt')

label_map = get_label_map_dict(LABEL_MAP_PATH)
label_array = [k for k in sorted(label_map, key=label_map.get)]

with open(os.path.join(labels_path, 'labels.json'), 'w') as f:
  json.dump(label_array, f)

data = {
    "model_type": str(MODEL_TYPE),
    "batch_size": int(TRAIN_BATCH_SIZE),
    "train_files_percent": float(TRAIN_FILES_PERCENT),
    "training_steps": int(NUM_TRAIN_STEPS)
}

f1 = open(labels_path+'\\'+'metadata.json','w')
f1.write(json.dumps(data))
f1.close()

