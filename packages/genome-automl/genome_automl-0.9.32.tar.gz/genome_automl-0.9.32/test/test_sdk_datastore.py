from unittest import TestCase
from unittest.mock import patch, MagicMock

import json
import logging

from .. import genome_automl

from ..genome_automl.models import modelstore
from ..genome_automl.datasets import datastore
from ..genome_automl.models import explainer
from ..genome_automl.models import estimator

from ..genome_automl.core.store import StoreContext
from ..genome_automl.core.base_entity import ModelArtifact, BaseRef, DataArtifact, Dataset, DataRef
from ..genome_automl.materializers.factory import MaterializerRegistry, DataFrameMaterializer


class TestDatastore(TestCase):

    @patch(datastore.__name__ + '.urllib.request.urlopen')
    def test_get_dataset(self, mock_urlopen):

        cm = MagicMock()
        cm.getcode.return_value = 200
        cm.read.return_value = """[{"id": "dataset-123",
          "application": "search",
          "canonicalName": "/search/pipeline",
          "schema": "schema-1",
          "versionName": "1.1",
          "specVersionName": "1.1",
          "pipelineName": "1.1",
          "pipelineStage":"papi",
          "pipelineRunId": "papi",
          "deployment": "papi-1",
          "specDeployment": "pipi-1",
          "dataRefs":[{"ref":"blob-123", "refType":"modelstore"}]}]"""
        cm.__enter__.return_value = cm

        cm1 = MagicMock()
        cm1.getcode.return_value = 200
        cm1.read.return_value = '{"id": "blob-123"}'
        cm1.__enter__.return_value = cm1


        mock_urlopen.side_effect = [cm]

        data_store = datastore.DataStore(StoreContext())
        #data_store.register_materializer(SklearnModelMaterializer())


        dataset = data_store.get_dataset({
          "canonicalName":"/search/pipeline",
          "application": "search"
        })

        mock_urlopen.assert_called()


        self.assertEqual(dataset.id, "dataset-123")

        # self.assertEqual(sum(2,3), 9)

        # testing metadata call with right extracted parameters
        self.assertEqual(len(mock_urlopen.call_args_list), 1)

        modelMeta = json.loads(mock_urlopen.call_args_list[0][0][1])
        self.assertEqual(dataset.application, "search")
        self.assertEqual(dataset.canonicalName, "/search/pipeline")



    @patch(datastore.__name__ + '.urllib.request.urlopen')
    def test_get_artifact(self, mock_urlopen):

        cm = MagicMock()
        cm.getcode.return_value = 200
        cm.read.return_value = """[{"id": "dataartifact-123",
          "application": "search",
          "canonicalName": "/search/pipeline",
          "target": "target-1",
          "dataset": "dataset-123",
          "format": "parquet",
          "versionName": "1.1",
          "specVersionName": "1.1",
          "datasetId": "dataset-123",

          "pipelineName": "1.1",
          "pipelineStage":"papi",
          "pipelineRunId": "papi",
          "deployment": "papi-1",
          "specDeployment": "pipi-1",
          "artifactStartTime": 0,
          "artifactTime": 0,
          "dataRefs":[{"ref":"blob-123", "refType":"modelstore"}]}]"""
        cm.__enter__.return_value = cm

        cm1 = MagicMock()
        cm1.getcode.return_value = 200
        cm1.read.return_value = '{"id": "blob-123"}'
        cm1.__enter__.return_value = cm1


        mock_urlopen.side_effect = [cm]

        data_store = datastore.DataStore(StoreContext())
        #data_store.register_materializer(SklearnModelMaterializer())

        dataset = Dataset(canonicalName = "canonical",
          application = "application",
          target = "pipiruqi",
          format = "funzzy-123", # [json, csv, parquet, avro, ]
          versionName = "fuzzy-123",
          schema = {})

        dataset.id = "dataset-123"


        data_artifacts = data_store.get_artifacts(dataset)

        mock_urlopen.assert_called()


        self.assertEqual(data_artifacts[0].id, "dataartifact-123")

        # self.assertEqual(sum(2,3), 9)

        # testing metadata call with right extracted parameters
        self.assertEqual(len(mock_urlopen.call_args_list), 1)


    @patch(datastore.__name__ + '.urllib.request.urlopen')
    def test_put_artifact(self, mock_urlopen):

        cm = MagicMock()
        cm.getcode.return_value = 200
        cm.read.return_value = """{"id": "dataartifact-123"}"""
        cm.__enter__.return_value = cm

        cm1 = MagicMock()
        cm1.getcode.return_value = 200
        cm1.read.return_value = '{"id": "blob-123"}'
        cm1.__enter__.return_value = cm1


        mock_urlopen.side_effect = [cm]

        data_store = datastore.DataStore(StoreContext())
        #data_store.register_materializer(SklearnModelMaterializer())



        dataset = DataArtifact(canonicalName = "canonical",
          application = "application",
          target = "pipiruqi",
          format = "parquet", # [json, csv, parquet, avro, ]
          versionName = "fuzzy-123",
          specVersionName = "1.2.3",
          datasetId = "dataset-123",
          pipelineName = "name-1",
          pipelineStage = "name-1",
          pipelineRunId = "name-1"
          )

        data_artifact_result = data_store.put_artifact(dataset)

        mock_urlopen.assert_called()


        self.assertEqual(data_artifact_result.id, "dataartifact-123")

        # self.assertEqual(sum(2,3), 9)

        # testing metadata call with right extracted parameters
        self.assertEqual(len(mock_urlopen.call_args_list), 1)




    @patch(datastore.__name__ + '.urllib.request.urlopen')
    def test_save_artifact(self, mock_urlopen):

        cm = MagicMock()
        cm.getcode.return_value = 200
        cm.read.return_value = """{"id": "dataartifact-123"}"""
        cm.__enter__.return_value = cm

        cm1 = MagicMock()
        cm1.getcode.return_value = 200
        cm1.read.return_value = '{"id": "blob-123"}'
        cm1.__enter__.return_value = cm1


        mock_urlopen.side_effect = [cm]

        MaterializerRegistry.registered_materializers = {}

        materializer_mock = DataFrameMaterializer()
        materializer_mock.SUPPORTED_TYPES = (object, )


        data_store = datastore.DataStore(StoreContext(bucket="buck"))
        data_store.register_materializer(materializer_mock)

        mat = data_store.get_materializer(list)

        logging.info(" ----- getting all the parts of the materializer: " +  str(type(mat)))

        self.assertTrue(mat == materializer_mock)



        dataset = DataArtifact(canonicalName = "canonical",
          application = "application",
          target = "pipiruqi",
          format = "parquet", # [json, csv, parquet, avro, ]
          versionName = "fuzzy-123",
          specVersionName = "1.2.3",

          datasetId = "dataset-123",
          pipelineName = "name-1",
          pipelineStage = "name-1",
          pipelineRunId = "name-1",
          artifactRef  = DataRef("ref-1", "type-1")
          )

        data_artifact_result = data_store.save([], dataset)

        mock_urlopen.assert_called()


        self.assertEqual(data_artifact_result.id, "dataartifact-123")

        # self.assertEqual(sum(2,3), 9)

        # testing metadata call with right extracted parameters
        self.assertEqual(len(mock_urlopen.call_args_list), 1)
