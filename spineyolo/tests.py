import time
from pathlib import Path

from django.test import TestCase

from spineyolo.prediction.SpineDetector import SpineDetector
from spineyolo.registry import MLRegistry

MODEL_PATH = Path("spineyolo/model")
WEIGHTS_PATH = MODEL_PATH / Path("weights")
STATIC_ROOT = Path("static/")


class MLTests(TestCase):
    def test_spineyolo_algorithm(self):
        input_data = {
            "image_path": 'static/tests/test_spines.jpg',
            "scale": 15,
        }
        predictor = SpineDetector(MODEL_PATH, WEIGHTS_PATH)
        predictor.set_root_dir(STATIC_ROOT.as_posix())
        predictor.start()
        predictor.set_local(True)
        predictor.set_inputs(input_data)
        u_id = time.strftime("%Y%m%d%H%M%S")
        predictor.queue.put(["find_spines", u_id])
        while u_id not in predictor.analyzed_spines.keys():
            continue
        results = predictor.analyzed_spines[u_id].tolist()
        self.assertTrue(1 < len(results) < 10)

    def test_registry(self):
        registry = MLRegistry()
        self.assertEqual(len(registry.endpoints), 0)
        endpoint_name = "spineyolo"
        algorithm_object = SpineDetector(MODEL_PATH, WEIGHTS_PATH)
        algorithm_name = "yolov3"
        algorithm_status = "production"
        algorithm_version = "0.0.1"
        algorithm_owner = "misha"
        algorithm_description = "yolov3 with pre and post " \
                                "processing for dendritic spine " \
                                "images and scales"
        algorithm_path = "path/to/algorithm"
        registry.add_algorithm(endpoint_name, algorithm_object, algorithm_name,
                               algorithm_status, algorithm_version, algorithm_owner,
                               algorithm_description, algorithm_path)
        self.assertEqual(len(registry.endpoints), 1)
