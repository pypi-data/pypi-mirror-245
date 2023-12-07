from unittest import TestCase
from unittest.mock import patch, MagicMock

import json
import os

from ..genome_automl.pipelines.flow_compiler import FlowCompilerFactory
from ..genome_automl.pipelines import step_annotations
from ..genome_automl.pipelines import flows

from ..genome_automl.pipelines.step_input import TransformInput, TransformOutput
from ..genome_automl.core.base_entity import ModelArtifact, TransformSpec, BaseRef, CodeRef


from .fixtures_pipelines import TestBranchingGraph, TestBranchingGraphWithTransform



class TestBranchingGraphRun(TestCase):
    def wrapper(o, func, *args, **kwargs):
        o.func(*args, **kwargs)


    def test_graph_run(self):

        graph = TestBranchingGraph({"input": "a"})
        graph.run()

        self.assertEqual(graph.step_calls['branch_dynamic'], 1)
        self.assertEqual(graph.step_calls['inside_foreach_step'], 6)

        self.assertEqual(True, 'condition_false_branch_step' in graph.step_calls)




    def test_graph_complier(self):

        graph = TestBranchingGraph({"input": "a"})

        genome_compiler = FlowCompilerFactory.get_compiler(graph, "genome")
        genome_compiled_flow = genome_compiler.compile()

        self.assertTrue(len(json.loads(genome_compiled_flow)), 6)
        self.assertTrue("condition" in genome_compiled_flow)

        json_compiler = FlowCompilerFactory.get_compiler(graph, "json")
        json_compiled_flow = json_compiler.compile()

        self.assertTrue(len(json.loads(json_compiled_flow)), 6)
        self.assertTrue("condition" in json_compiled_flow)


    @patch(step_annotations.__name__ + '.subprocess.Popen')
    def test_graph_run_image(self, mock_subprocess):


        transformOutput = TransformOutput([

            ModelArtifact(

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

        ], None)

        input_str = transformOutput.get_meta()

        cm = MagicMock()
        cm.communicate.return_value = (json.dumps(input_str).encode("utf-8"), None)

        mock_subprocess.side_effect = [cm]


        graph = TestBranchingGraphWithTransform({"input": "a"})
        graph.run()

        mock_subprocess.assert_called()

        self.assertEqual(graph.step_calls['branch_metrics'], 1)
        self.assertEqual(graph.step_calls['metrics_1'], 1)



    @patch(flows.__name__ + '.urllib.request.urlopen')
    def test_graph_run_remote(self, mock_urlopen):

        # defines what is the next step
        transformInput = TransformInput([], TransformSpec(
          canonicalName = "first/flow/transform-start",
          application = "search",

          code = CodeRef("ecr://my-first-image:latest", "docker"),

          framework = "tensorflow",
          inputModality = "image",

          versionName = "1.0.23", # version name of the whole config for this model
          specVersionName = "1.1.5"

        ), None)

        os.environ['CALLBACK_URL'] = 'http://someurl.com'
        os.environ['STEP_NAME'] = 'check_to_proceed'
        os.environ['STEP_INPUT'] = json.dumps(transformInput.get_meta())

        graph = TestBranchingGraph({"input": "a"})
        graph.run()

        mock_urlopen.assert_called()
