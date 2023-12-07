from typing import Mapping, List, Tuple, Dict, Any

import json
import logging
import datetime

import io
import base64
import tempfile
import uuid

from ..core.base_entity import BaseRef, CodeRef, DataRef, Segment, ArtifactMeta, BaseMetric


class CardArtifact(ArtifactMeta):

    def __init__(self,

      canonicalName: str = None,
      application: str = None,
      target: str = None,

      pipelineName: str = None,
      pipelineRunId: str = None,
      pipelineStage: str = None,

      code: CodeRef = None,


      versionName: str = None, # version name of the whole config for this model
      specVersionName: str = None, # version name of the code/template for this model

      deployment: str = None, # whole config/spec deployment, which changes even if template is same
      specDeployment: str = None, # template config/spec deployment

      dataRefs: List[DataRef] = None,

      format: str = None, # [json, csv, parquet, avro, ]

      dimension: str = None, # same as an evaluation, cards play to quality dimensions

      cardTarget: BaseRef = None, # what the card is for evaluation, model, data

      artifactBlob: BaseRef = None, # pointer to raw files in storage

      startTime: datetime.datetime = None, #lower time bound of the data contained in this artifact
      endTime: datetime.datetime = None, #upper time bound of the data contained in this artifact

      tags: dict = None,
      context: dict = None):

        self.canonicalName = canonicalName
        self.application = application
        self.target = target

        self.pipelineName = pipelineName
        self.pipelineRunId = pipelineRunId
        self.pipelineStage = pipelineStage

        self.code = code

        self.versionName = versionName
        self.specVersionName = specVersionName

        self.deployment = deployment
        self.specDeployment = specDeployment

        self.dataRefs = dataRefs

        self.format = format
        self.dimension = dimension

        self.cardTarget = cardTarget


        self.artifactBlob = artifactBlob

        self.tags = tags
        self.context = context

        self.id = None # this should be set only when retrieving artifacts from DB, not on instantiation


class HtmlComponent():
    def to_html(self):
        pass


class Card(HtmlComponent):

    def __init__(self, header, content):
        self.header = header
        self.content = content


    def to_html(self):
        return (
                 f"<html>"
                 f"<div class=\"genomeCard\">"
                 f"{self.header.to_html()}"
                 f"{self.content.to_html()}"
                 f"</div>"
                 f"</html>"
               )


class Header(HtmlComponent):

    def __init__(self, title):
        self.header = title

    def to_html(self):
        return f"<h1 class=\"titleCard\">{self.header}</h1>"


class Table(HtmlComponent):

    def __init__(self, rows):
        self.rows = rows or []

    def append(self, row):
        self.rows.append(row)

    def to_html(self):
        return f"<div class=\"tableCard\">{''.join([a.to_html() for a in self.rows])}</div>"


class Row(HtmlComponent):

    def __init__(self, columns:List[HtmlComponent]):
        self.columns = columns or []

    def append(self, col):
        self.columns.append(col)


    def to_html(self):
        import math
        width_percentage = math.floor(100 / max(1, len(self.columns or [])))

        return f"<div class=\"rowCard\">{''.join([a.to_html(width = width_percentage) for a in self.columns])}</div>"



class Column(HtmlComponent):
    def __init__(self, content:HtmlComponent):
        self.content = content

    def to_html(self, width = 100):
        return f"<div class=\"colContentCard\" style=\"width:{width}%;\">{self.content.to_html()}</div>"



class IFrameComponent(HtmlComponent):
    def __init__(self, width:int, height:int, content:str):
        self.width = width
        self.height = height
        self.content = content

    def to_html(self):
        return (f"<div class=\"iframeContentCard\" style=\"width:{self.width}px;height:{self.height}px;\">"
               f"<iframe style=\"width:{self.width}px;height:{self.height}px;border:0px;\">"
               f"src=\"{self.content}\""
               f"</iframe>"
               f"</div>")



class ArtifactComponent(HtmlComponent):

    def __init__(self, artifact: ArtifactMeta = None):
        self.artifact = artifact

    def to_html(self):
        meta = self.artifact.get_meta()
        return (f"<div class=\"artifactComponent\">"
        f"<div class=\"artifactType\">{type(self.artifact).__name__}</div>"
        f"{self._prop_html(meta)}"
        f"</div>")


    def _prop_html(self, val: Any):
        result = ""
        if type(val) in [dict, list]:
            val_iterable = val.items() if type(val) == dict else enumerate(val)
            for k, v in val_iterable:
                result += (f"<div class=\"artifactKV\">"
                       f"<div class=\"artifactK\">{str(k)}</div>"
                       f"{self._prop_html(v)}"
                       f"</div>")

        elif type(val) in [int, float, bool, str]:
            result = f"<div class=\"artifactV\">{str(val)}</div>"

        return result





class InnerHtml(HtmlComponent):
    def __init__(self, content):
        self.content = content

    def to_html(self):
        return f"<div class=\"innerHtmlCard\">{self.content}</div>"
