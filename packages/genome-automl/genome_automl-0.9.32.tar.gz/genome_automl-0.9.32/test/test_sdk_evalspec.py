from unittest import TestCase, TestSuite, TextTestRunner
from unittest.mock import patch, MagicMock

import sys
import io
import json
import pickle
import logging

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


from .fixtures import TrainTestEvaluation

from ..genome_automl.core.store import StoreContext

from ..genome_automl.evaluations import evaluationstore


class TestEvaluationRunSpec(TestCase):

    def test_spec_run(self):

        store = MagicMock()
        store.save.return_value = {}
        eval_ml = TrainTestEvaluation(store, validationTarget = "model-uuid")
        eval_run = eval_ml.to_run()

        store.save.assert_called()
        # self.assertEqual(sum(2,3), 9)

        num_tasks = len(eval_run.tasks)

        # 3 tasks from functions plus 5 from prototypes
        self.assertEqual(num_tasks, 8)

        self.assertEqual(eval_run.tasks[0]["name"], "evaluateTrainTestSplit")
        self.assertEqual(eval_run.tasks[0]["metrics"]["f2"], 2.34)
        self.assertEqual(len(eval_run.tasks[0]["expectations"]), 1)

        self.assertEqual(eval_run.canonicalName, "test/skill/annotations/better-than-last")
        self.assertEqual(eval_run.validationTarget["ref"], "model-uuid")



    @patch(evaluationstore.__name__ + '.urllib.request.urlopen')
    def test_evaluation_meta_load(self, mock_urlopen):

        evaluation_store = evaluationstore.EvaluationStore(StoreContext())

        cm = MagicMock()
        cm.getcode.return_value = 200
        cm.read.return_value = '[{"artifactType": "evaluationArtifact", "id": "eval-123"}]'
        cm.__enter__.return_value = cm

        mock_urlopen.side_effect = [cm]

        eval_artifact = evaluation_store.load({"canonicalName": "something"})
        self.assertEqual(eval_artifact["id"], "eval-123")

        mock_urlopen.assert_called()



    @patch(evaluationstore.__name__ + '.urllib.request.urlopen')
    def test_evaluation_save(self, mock_urlopen):

        store = MagicMock()
        store.save.return_value = {}
        eval_ml = TrainTestEvaluation(store, validationTarget = "model-uuid")
        eval_artifact = eval_ml.to_run()

        store.save.assert_called()


        evaluation_store = evaluationstore.EvaluationStore(StoreContext())

        cm = MagicMock()
        cm.getcode.return_value = 200
        cm.read.return_value = '{"id": "eval-123"}'
        cm.__enter__.return_value = cm

        mock_urlopen.side_effect = [cm]

        eval_artifact = evaluation_store.save(eval_artifact)
        self.assertEqual(eval_artifact.id, "eval-123")

        mock_urlopen.assert_called()


    @patch(evaluationstore.__name__ + '.urllib.request.urlopen')
    def test_evaluation_to_artifact(self, mock_urlopen):

        store = MagicMock()
        store.save.return_value = {}
        eval_ml = TrainTestEvaluation(store, validationTarget = "model-uuid")
        eval_artifact = eval_ml.to_run()

        store.save.assert_called()

        cm = MagicMock()
        cm.getcode.return_value = 200
        cm.read.return_value = '{"id": "eval-123"}'
        cm.__enter__.return_value = cm

        mock_urlopen.side_effect = [cm]

        meta_artifact = eval_artifact.get_meta()


        evaluation_store = evaluationstore.EvaluationStore(StoreContext())

        evaluation_store._dict_to_artifact(meta_artifact)



        eval_artifact = evaluation_store.save(eval_artifact)

        self.assertEqual(eval_artifact.canonicalName, "test/skill/annotations/better-than-last")
        self.assertEqual(eval_artifact.versionName, "1.2.sklearn")
        self.assertEqual(eval_artifact.id, "eval-123")

        mock_urlopen.assert_called()
