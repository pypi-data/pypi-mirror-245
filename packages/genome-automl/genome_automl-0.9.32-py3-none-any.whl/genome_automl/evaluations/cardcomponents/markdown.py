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


class Markdown(HtmlComponent):
    def __init__(self, content):
        self.content = content

    def to_html(self):
        import markdown
        return f"<div class=\"markdownCard\">{markdown.markdown(self.content)}</div>"
