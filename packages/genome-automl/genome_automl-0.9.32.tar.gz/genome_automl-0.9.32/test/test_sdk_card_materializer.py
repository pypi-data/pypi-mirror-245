from unittest import TestCase
from unittest.mock import patch, MagicMock

import sys
import io
import json
import pickle
import logging


from .. import genome_automl

from ..genome_automl.models import modelstore
from ..genome_automl.evaluations import evaluationstore

from ..genome_automl.core.store import StoreContext
from ..genome_automl.core.base_entity import ModelArtifact, BaseRef, CodeRef

from ..genome_automl.evaluations.card import CardArtifact, Card, Header, Table, Row, Column, InnerHtml
from ..genome_automl.evaluations.evaluationspec import EvaluationDimension

from ..genome_automl.materializers.factory import MaterializerRegistry
from ..genome_automl.materializers import card_html_materializer

from ..genome_automl.materializers.card_html_materializer import CardHTMLMaterializer



class TestCardMaterializer(TestCase):

    @patch(evaluationstore.__name__ + '.urllib.request.urlopen')
    def test_save_card(self, mock_urlopen):

        cm = MagicMock()
        cm.getcode.return_value = 200
        cm.read.return_value = '{"id": "blob-123"}'
        cm.__enter__.return_value = cm

        cm1 = MagicMock()
        cm1.getcode.return_value = 200
        cm1.read.return_value = '{"id": "model-123"}'
        cm1.__enter__.return_value = cm1


        mock_urlopen.side_effect = [cm, cm1]


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


        header = Header("component-header")
        table = Table([Row([Column(InnerHtml("plot-with-model"))])])

        card = Card(header, table)

        ctx = StoreContext()
        evaluation_store = evaluationstore.EvaluationStore(ctx)

        MaterializerRegistry.registered_materializers = {}

        mock_materializer = CardHTMLMaterializer()
        prev_types = mock_materializer.SUPPORTED_TYPES
        mock_materializer.SUPPORTED_TYPES = (object, )

        evaluation_store.register_materializer(mock_materializer)
        evaluation_store.save_card(card, card_artifact)


        mock_urlopen.assert_called()
        # self.assertEqual(sum(2,3), 9)

        # testing metadata save being called with right extracted parameters
        evalMeta = json.loads(mock_urlopen.call_args_list[1][0][1])
        self.assertEqual(evalMeta["application"], "search")
        self.assertEqual(evalMeta["pipelineName"], "pipeline-sklearn-test")

        mock_materializer.SUPPORTED_TYPES = prev_types
