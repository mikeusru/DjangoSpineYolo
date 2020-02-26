import time
from pathlib import Path

from django.test import TestCase

from spineyolo.prediction.SpineDetector import SpineDetector


class MLTests(TestCase):
    def test_spineyolo_algorithm(self):
        input_data = {
            "image_path": 'static/test/test_spines.jpg',
            "scale": 15,
        }
        MODEL_PATH = Path("spineyolo/model")
        WEIGHTS_PATH = MODEL_PATH / Path("weights")
        STATIC_ROOT = Path("static/")
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
        self.assertEqual(len(results), 5)
