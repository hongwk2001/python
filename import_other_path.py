import os.path
import sys

sys.path.append(os.path.join(os.path.curdir, 'run_folder'))

import temp
import dict_test

print(temp.to_celsius(95))