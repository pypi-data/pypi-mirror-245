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
import uuid

import warnings



class EvidentlyComponent(HtmlComponent):

    def __init__(self, report = None, reference_data = None, current_data = None):
        self.report = report
        self.reference = reference_data
        self.current = current_data


    def to_html(self):

        self.report.run(reference_data=self.reference, current_data=self.current)

        tmpdir = tempfile.mkdtemp()
        file_report_path = tmpdir + "/report_file.html"

        self.report.save_html(file_report_path)

        file_obj = open(file_report_path, 'r')
        raw_html = file_obj.read()
        file_obj.close()

        component_iframe_id = str(uuid.uuid4())

        raw_html = raw_html.replace("format('woff2');", "format(\"woff2\");")
        raw_html = raw_html.replace("'Material Icons'", "\"Material Icons\"")
        #bug in evidtly
        raw_html += "</html>"

        base64_html_data = base64.b64encode(raw_html.encode('utf-8'))



        width = None
        height = 1000
        sizing = f"style=\"width:{100}%;min-height:{height}px;border:0px\"" if not width else f"style=\"width:{width}px;height:{height}px;\""

        all_container = f"<div class=\"evdlyComponent\">";


        # encode content as base64 so we do not have parsing problems because of enclosing quotes;
        # then use createObjectURL from javascript to circimvent brwoser size limits
        all_container += ("<iframe onload=\"(e)=>{console.log('onload evdtly iframe:', e); e.target.style.height=(e.target.contentDocument.body.scrollHeight + 245) + 'px';}\" "
                         f"id=\"evdtlComponent_{component_iframe_id}\" {sizing} "
                         f"src=\"about:blank()\"></iframe>");

        all_container += (f"<script type='text/javascript'>\n"
            "function dataURLtoBlob(dataurl) {\n"
            "    console.log('called dataUrl with length:', dataurl.length);\n"
            "    var mime = \"text/html\","
            "        bstr = atob(dataurl), n = bstr.length, u8arr = new Uint8Array(n);\n"
            "    while(n--){\n"
            "        u8arr[n] = bstr.charCodeAt(n);\n"
            "    }\n"
            "    return new Blob([u8arr], {type:mime});\n"
            "}\n"
            f"var evdtlyComp_data_uri = \"{base64_html_data.decode('utf-8')}\";\n"
            f"var iframeBlob = dataURLtoBlob(evdtlyComp_data_uri);\n"
            f"var temp_url = URL.createObjectURL(iframeBlob);\n"
            f"console.log('called createObjectURL with result length:', temp_url.length);\n"
            f"document.getElementById(\"evdtlComponent_{component_iframe_id}\").src = temp_url;\n"
            f"</script>"
        )
        all_container += "</div>"

        return all_container
