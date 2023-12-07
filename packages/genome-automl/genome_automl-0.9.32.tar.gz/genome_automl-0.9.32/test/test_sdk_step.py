from unittest import TestCase
from unittest.mock import patch, MagicMock

from ..genome_automl.core.base_entity import ModelArtifact, TransformSpec, BaseRef, CodeRef


from ..genome_automl.pipelines.step_input import PushModelInput, QueryInput, QueryOutput

from ..genome_automl.pipelines.steps import call_steps
from ..genome_automl.pipelines.steps.call_steps import QueryStep, PushStep


class TestSteps(TestCase):

    @patch(call_steps.__name__ + '.urllib.request.urlopen')
    def test_push_step(self, mock_urlopen):

        cm = MagicMock()
        cm.getcode.return_value = 200
        cm.read.return_value = '{"id": "model-123"}'
        cm.__enter__.return_value = cm

        mock_urlopen.side_effect = [cm]

        artifact = ModelArtifact(
          application = "search",
          canonicalName = "/search/pipeline",
          framework = "tensorflow",
          versionName = "1.1",
          specVersionName = "1.1",
          pipelineName = "pipe-1.1",
          pipelineStage = "papi",
          pipelineRunId = "papi",
          deployment = "papi-1",
          specDeployment = "pipi-1",
          artifactBlob = BaseRef("blob-123", "modelstore")
        )


        push_model_input = PushModelInput(artifact)

        push_step = PushStep("pushmodel")
        step_out = push_step.push_entry(push_model_input)

        self.assertEqual(step_out.model_artifact.canonicalName, "/search/pipeline")


    @patch(call_steps.__name__ + '.urllib.request.urlopen')
    def test_query_step(self, mock_urlopen):

        cm = MagicMock()
        cm.getcode.return_value = 200
        cm.read.return_value = """[{"id": "model-123",
          "application": "search",
          "canonicalName": "/search/pipeline",
          "framework":"sklearn",
          "versionName": "1.1",
          "specVersionName": "1.1",
          "pipelineName": "1.1",
          "pipelineStage":"papi",
          "pipelineRunId": "papi",
          "deployment": "papi-1",
          "specDeployment": "pipi-1",
          "artifactBlob":{"ref":"blob-123", "refType":"modelstore"}}]"""
        cm.__enter__.return_value = cm

        mock_urlopen.side_effect = [cm]

        query_input = QueryInput({"query": "some-id"})

        query_step = QueryStep("querymodel")
        step_out = query_step.query(query_input)

        mock_urlopen.assert_called()

        self.assertEqual(type(step_out), QueryOutput)
