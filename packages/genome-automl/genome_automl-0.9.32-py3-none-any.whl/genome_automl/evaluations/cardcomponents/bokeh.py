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



class BokehComponent(HtmlComponent):

    def __init__(self, fig = None):
        self.fig = fig

    def to_html(self):
        from bokeh.embed import components
        script, div = components(self.fig)

        width = (self.fig.width + 5) if getattr(self.fig, "width", None) else None
        height = (self.fig.height + 20) if getattr(self.fig, "height", None) else None
        sizing = "" if not width else f"style=\"width:{width}px;height:{height}px;border:0px;\""

        all_container = f"<div class=\"bokehComponent\">";

        html_container = f"<script src=\"https://cdn.bokeh.org/bokeh/release/bokeh-3.0.1.min.js\" crossorigin=\"anonymous\"></script>";
        html_container += script.replace("'", "`");
        html_container += div;

        all_container += f"<iframe {sizing} srcdoc='{html_container}'></iframe>";
        all_container += "</div>"

        return all_container
