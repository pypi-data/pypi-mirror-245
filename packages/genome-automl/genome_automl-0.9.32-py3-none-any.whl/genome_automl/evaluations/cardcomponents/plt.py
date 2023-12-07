from typing import Mapping, List, Tuple, Dict, Type, Union, Any
from enum import Enum

from ..card import HtmlComponent


import json
import logging
import sys
import time
import os
import os.path
import pickle
import urllib.request
from urllib.error import  URLError
import base64
import io
import glob
import tempfile
import zipfile
import shutil

import warnings


class PltImage(HtmlComponent):

    def __init__(self, fig = None):
        self.fig = fig


    def to_html(self):

        from matplotlib import pyplot as plt

        my_string_io_bytes = io.BytesIO()

        fig = self.fig or plt
        fig.savefig(my_string_io_bytes, format='jpg')

        my_string_io_bytes.seek(0)
        base64_jpgData = base64.b64encode(my_string_io_bytes.read())

        return f'<img class="imgCard" src="data:image/jpeg;base64,{base64_jpgData.decode()}" />'
