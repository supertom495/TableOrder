import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")
import common
import updateProducts
import api

common.setVar()
updateProducts.uploadImageToAPI()