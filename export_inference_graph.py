import os
import re
import sys

OUTPUT_PATH = sys.argv[1]
regex = re.compile(r"ckpt-([0-9]+)\.index")
numbers = [int(regex.search(f).group(1)) for f in os.listdir(OUTPUT_PATH) if regex.search(f)]
TRAINED_CHECKPOINT_PREFIX = os.path.join(OUTPUT_PATH, 'ckpt-{}'.format(max(numbers)))
#TRAINED_CHECKPOINT_PREFIX = os.path.join(OUTPUT_PATH)
print(f'Using {TRAINED_CHECKPOINT_PREFIX}')
f = open("temp.txt", "w")
f.write(TRAINED_CHECKPOINT_PREFIX)
f.close()
