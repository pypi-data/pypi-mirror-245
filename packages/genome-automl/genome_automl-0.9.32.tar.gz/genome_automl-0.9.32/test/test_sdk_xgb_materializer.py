from unittest import TestCase
from unittest.mock import patch, MagicMock

import sys
import io
import json
import pickle
import logging


from .. import genome_automl

from ..genome_automl.core.store import StoreContext
from ..genome_automl.core.base_entity import ModelArtifact, BaseRef, CodeRef

from ..genome_automl.models import modelstore
from ..genome_automl.models import meta_extractor

from ..genome_automl.evaluations import evaluationstore
from ..genome_automl.evaluations.evaluationspec import EvaluationDimension

from ..genome_automl.materializers.factory import MaterializerRegistry
from ..genome_automl.materializers import model_xgboost_materializer



class TestXGBoostMaterializer(TestCase):

    @patch(modelstore.__name__ + '.ExtractorFactory')
    @patch(modelstore.__name__ + '.urllib.request.urlopen')
    def test_save_xgboost(self, mock_urlopen, mock_extractor_factory):

        cm = MagicMock()
        cm.getcode.return_value = 200
        cm.read.return_value = '{"id": "blob-123"}'
        cm.__enter__.return_value = cm

        cm1 = MagicMock()
        cm1.getcode.return_value = 200
        cm1.read.return_value = '{"id": "model-123"}'
        cm1.__enter__.return_value = cm1


        mock_urlopen.side_effect = [cm, cm1]

        artifact = ModelArtifact(
          application = "search",
          canonicalName = "/search/pipeline",
          framework = "xgboost",
          versionName = "1.1",
          specVersionName = "1.1",
          pipelineName = "pipe-1.1",
          pipelineStage = "papi",
          pipelineRunId = "papi",
          deployment = "papi-1",
          specDeployment = "pipi-1",
          artifactBlob = BaseRef("blob-123", "modelstore")
        )

        artifact.id = "model-123"

        model_mock = MagicMock()
        model_mock.__type__ = "xgboost"
        model_mock.save_model.return_value = "xgboost"

        mock_extractor_factory.get_parameter_extractor.return_value = meta_extractor.XGMetaExtractor()

        MaterializerRegistry.registered_materializers = {}

        ctx = StoreContext()
        model_store = modelstore.ModelStore(ctx)

        mock_materializer = model_xgboost_materializer.XGBoostModelMaterializer()
        prev_types = mock_materializer.SUPPORTED_TYPES
        mock_materializer.SUPPORTED_TYPES = (object, )

        model_store.register_materializer(mock_materializer)


        model_store.save(model_mock, artifact)


        mock_urlopen.assert_called()

        model_mock.save_model.assert_called()
        # self.assertEqual(sum(2,3), 9)

        # testing metadata save being called with right extracted parameters
        modelMeta = json.loads(mock_urlopen.call_args_list[1][0][1])
        self.assertEqual(modelMeta["application"], "search")
        self.assertEqual(modelMeta["pipelineName"], "pipe-1.1")
        self.assertEqual(modelMeta["framework"], "xgboost")

        mock_materializer.SUPPORTED_TYPES = prev_types


    @patch(model_xgboost_materializer.__name__ + '.zipfile.ZipFile')
    @patch(modelstore.__name__ + '.urllib.request.urlopen')
    def test_load_xgboost_model(self, mock_urlopen, mock_zip):

        cm = MagicMock()
        cm.getcode.return_value = 200
        cm.read.return_value = """[{"id": "model-123",
          "application": "search",
          "canonicalName": "/search/pipeline",
          "framework":"xgboost",
          "versionName": "1.1",
          "specVersionName": "1.1",
          "pipelineName": "1.1",
          "pipelineStage":"papi",
          "pipelineRunId": "papi",
          "deployment": "papi-1",
          "specDeployment": "pipi-1",
          "artifactBlob":{"ref":"blob-123", "refType":"modelstore"}}]"""
        cm.__enter__.return_value = cm

        cm1 = MagicMock()
        cm1.getcode.return_value = 200
        cm1.read.return_value = b""
        cm1.__enter__.return_value = cm1


        model_xgboost_materializer.xgboost = MagicMock()

        model_xgboost_materializer.xgboost.Booster = MagicMock()
        model_xgboost_materializer.xgboost.Booster.load_model.return_value = 3

        mock_zip.namelist.return_value = '["file-1"]'
        mock_zip.extractall.return_value = "no-op"



        mock_urlopen.side_effect = [cm, cm1]

        MaterializerRegistry.registered_materializers = {}

        model_store = modelstore.ModelStore(StoreContext())

        mock_materializer = model_xgboost_materializer.XGBoostModelMaterializer()
        prev_types = mock_materializer.SUPPORTED_TYPES
        mock_materializer.SUPPORTED_TYPES = (object, )

        model_store.register_materializer(mock_materializer)

        model, meta = model_store.load_model({
          "canonicalName":"/search/pipeline",
          "application": "search"
        }, withMeta=True)

        mock_urlopen.assert_called()
        model_xgboost_materializer.xgboost.Booster.assert_called()


        self.assertEqual(meta["id"], "model-123")

        # self.assertEqual(sum(2,3), 9)

        # testing metadata call with right extracted parameters
        self.assertEqual(len(mock_urlopen.call_args_list), 2)

        modelMeta = json.loads(mock_urlopen.call_args_list[0][0][1])
        self.assertEqual(modelMeta["application"], "search")
        self.assertEqual(modelMeta["canonicalName"], "/search/pipeline")


        mock_materializer.SUPPORTED_TYPES = prev_types
