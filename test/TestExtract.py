import unittest

import sys
sys.path.insert(0, sys.path[0][:-5])

for i in sys.path:
    print(i)

# from extract import json2dict
from Football_API.extract import json2dict
