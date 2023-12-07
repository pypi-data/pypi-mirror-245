from unittest import TestCase
from unittest.mock import patch, MagicMock

from ..genome_automl.core.base_entity import ModelArtifact, DataArtifact, BaseRef, CodeRef, DataRef
from ..genome_automl.evaluations.card import CardArtifact

from ..genome_automl.pipelines.step_input import StepInput, TransformInput, TransformOutput, DataTransformInput, DataTransformOutput
from ..genome_automl.pipelines.step_input import CardTransformOutput, PushModelInput, PushDataArtifactInput
from ..genome_automl.pipelines.step_input import PushEvaluationInput, PushCardInput, PushPipelineInput, QueryInput, QueryOutput

from ..genome_automl.evaluations.evaluationspec import EvaluationDimension, GenomeEvaluationRun, evaluation, task

class TestStepInput(TestCase):

    def test_step_input(self):

        model_artifact = ModelArtifact(

          canonicalName = "first/flow/transform-train",
          application = "search",

          code = CodeRef("ecr://my-first-image:latest", "docker"),

          framework = "tensorflow",
          inputModality = "image",

          versionName = "1.0.23", # version name of the whole config for this model
          specVersionName = "1.1.5",

          pipelineName = "python-flow",
          pipelineRunId = "whatever-1",
          pipelineStage = "train",

          deployment = "deployment-abcd",
          specDeployment = "1.2.3-test",

          artifactBlob = BaseRef("uuid-123456", "modelstore")

        )

        data_artifact = DataArtifact(canonicalName = "canonical",
          application = "application",
          target = "pipiruqi",
          format = "parquet", # [json, csv, parquet, avro, ]
          datasetId = "name-1",
          versionName = "fuzzy-123",
          specVersionName = "1.2.3",
          pipelineName = "name-1",
          pipelineStage = "name-1",
          pipelineRunId = "name-1",
          artifactRef  = DataRef("ref-1", "type-1")
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


        transform_input = TransformInput([], model_artifact ,[])
        transform_output = TransformOutput([model_artifact], [])

        data_transform_input = DataTransformInput([], model_artifact, [])
        data_transform_output = DataTransformOutput([], [])

        card_transform_output = CardTransformOutput([])


        push_model_input = PushModelInput(model_artifact)
        push_artifact_input = PushDataArtifactInput(data_artifact)

        push_evaluation_input = PushEvaluationInput(card_artifact)
        push_card_input = PushCardInput(card_artifact)

        push_pipeline_input = PushPipelineInput({"pipeline": "pipe-123"})

        query_input = QueryInput({"query": "all"})
        query_output = QueryOutput([data_artifact])

        self.assertTrue("cls_name" in query_input.get_meta() and query_input.get_meta()["cls_name"])
        self.assertTrue("cls_name" in query_output.get_meta() and query_output.get_meta()["cls_name"])

        self.assertTrue("cls_name" in push_pipeline_input.get_meta() and push_pipeline_input.get_meta()["cls_name"])

        self.assertTrue("cls_name" in push_card_input.get_meta() and push_card_input.get_meta()["cls_name"])
        self.assertTrue("cls_name" in push_evaluation_input.get_meta() and push_evaluation_input.get_meta()["cls_name"])

        self.assertTrue("cls_name" in push_artifact_input.get_meta() and push_artifact_input.get_meta()["cls_name"])
        self.assertTrue("cls_name" in push_model_input.get_meta() and push_model_input.get_meta()["cls_name"])

        self.assertTrue("cls_name" in data_transform_input.get_meta() and data_transform_input.get_meta()["cls_name"])
        self.assertTrue("cls_name" in data_transform_output.get_meta() and data_transform_output.get_meta()["cls_name"])

        self.assertTrue("cls_name" in transform_input.get_meta() and transform_input.get_meta()["cls_name"])
        self.assertTrue("cls_name" in transform_output.get_meta() and transform_output.get_meta()["cls_name"])



        self.assertTrue(StepInput.from_meta(query_input.get_meta())._cls_name, query_input._cls_name)
        self.assertTrue(StepInput.from_meta(query_output.get_meta())._cls_name, query_output._cls_name)

        self.assertTrue(StepInput.from_meta(push_pipeline_input.get_meta())._cls_name, push_pipeline_input._cls_name)

        self.assertTrue(StepInput.from_meta(push_card_input.get_meta())._cls_name, push_card_input._cls_name)
        self.assertTrue(StepInput.from_meta(push_evaluation_input.get_meta())._cls_name, push_evaluation_input._cls_name)

        self.assertTrue(StepInput.from_meta(push_artifact_input.get_meta())._cls_name, push_artifact_input._cls_name)
        self.assertTrue(StepInput.from_meta(push_model_input.get_meta())._cls_name, push_model_input._cls_name)

        self.assertTrue(StepInput.from_meta(data_transform_input.get_meta())._cls_name, data_transform_input._cls_name)
        self.assertTrue(StepInput.from_meta(data_transform_output.get_meta())._cls_name, data_transform_output._cls_name)

        self.assertTrue(StepInput.from_meta(transform_input.get_meta())._cls_name, transform_input._cls_name)
        self.assertTrue(StepInput.from_meta(transform_output.get_meta())._cls_name, transform_output._cls_name)


        self.assertEquals(transform_input.get_meta()["transform_spec"]["framework"], "tensorflow")
        self.assertEquals(StepInput.from_meta(transform_input.get_meta()).transform_spec.specVersionName, transform_input.transform_spec.specVersionName)
