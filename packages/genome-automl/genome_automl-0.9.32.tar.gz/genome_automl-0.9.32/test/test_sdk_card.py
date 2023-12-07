
from unittest import TestCase
from unittest.mock import patch, MagicMock

import base64

from ..genome_automl.core.base_entity import ModelArtifact, BaseRef, CodeRef

from ..genome_automl.evaluations import card

from ..genome_automl.evaluations.card import CardArtifact, ArtifactComponent, Card, Header, Table, Row, Column, InnerHtml
from ..genome_automl.evaluations.cardcomponents import EvidentlyComponent
from ..genome_automl.evaluations.evaluationspec import EvaluationDimension

from ..genome_automl.models import estimator



class TestCard(TestCase):

    def test_card_component(self):

        model_artifact = ModelArtifact(
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

        card_artifact = CardArtifact(
            canonicalName = "/canon/search-1",
            application = "search",
            code = CodeRef("ecr://code-ref/search-1", "docker"),

            pipelineName = "pipeline-sklearn-test",
            pipelineRunId = "run-id-123",
            pipelineStage = "model-hpo",

            versionName = "sklearn.1.2.2",
            specVersionName = "template-0.0.5",

            deployment = "",
            specDeployment = "deployment-0.0.1",
            format = "html",
            dimension = EvaluationDimension.PERFORMANCE.value,

            cardTarget = BaseRef("id-artifact", "model"))

        artifact_cmp = ArtifactComponent(artifact = model_artifact)
        artifact_html = artifact_cmp.to_html()

        self.assertTrue("tensorflow" in artifact_html)

        self.assertEqual(card_artifact.get_meta()["specDeployment"], "deployment-0.0.1")
        self.assertEqual(card_artifact.get_meta()["dimension"], "PERFORMANCE")



    def test_card(self):

        header = Header("component-header")
        table = Table([Row([Column(InnerHtml("plot-with-model"))])])

        card = Card(header, table)

        self.assertTrue("plot-with-model" in card.to_html())



    #@patch(card.__name__ + '.plt')
    @patch('builtins.open')
    def test_card_evidently(self, mock_open_file):


        evdtly_mock = MagicMock()
        evdtly_mock.run.return_value = ""
        evdtly_mock.save_html.return_value = ""

        evdently_html_report = """<html>evidently-mock</html>"""
        file_mock = MagicMock()
        file_mock.read.return_value = evdently_html_report

        mock_open_file.return_value = file_mock

        header = Header("component-header")
        table = Table([Row([Column(EvidentlyComponent(evdtly_mock))])])

        card = Card(header, table)

        base64_html_data = base64.b64encode(evdently_html_report.encode('utf-8'))


        self.assertTrue(base64_html_data.decode("utf-8") in card.to_html())
