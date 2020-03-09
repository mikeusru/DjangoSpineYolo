import time
from pathlib import Path

from channels.testing import ChannelsLiveServerTestCase
from django.test import TestCase
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait

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
        predictor = SpineDetector(MODEL_PATH, WEIGHTS_PATH, STATIC_ROOT)
        predictor.set_local(True)
        predictor.set_inputs(input_data)
        u_id = time.strftime("%Y%m%d%H%M%S")
        predictor.queue.put(["find_spines", u_id])
        while u_id not in predictor.analyzed_spines.keys():
            continue
        results = predictor.analyzed_spines[u_id].tolist()
        self.assertTrue(1 < len(results) < 10)
    #
    # def test_registry(self):
    #     registry = MLRegistry()
    #     self.assertEqual(len(registry.endpoints), 0)
    #     endpoint_name = "spineyolo"
    #     algorithm_object = SpineDetector(MODEL_PATH, WEIGHTS_PATH, STATIC_ROOT)
    #     algorithm_name = "yolov3"
    #     algorithm_status = "production"
    #     algorithm_version = "0.0.1"
    #     algorithm_owner = "misha"
    #     algorithm_description = "yolov3 with pre and post " \
    #                             "processing for dendritic spine " \
    #                             "images and scales"
    #     algorithm_path = "path/to/algorithm"
    #     registry.add_algorithm(endpoint_name, algorithm_object, algorithm_name,
    #                            algorithm_status, algorithm_version, algorithm_owner,
    #                            algorithm_description, algorithm_path)
    #     self.assertEqual(len(registry.endpoints), 1)


class AnalysisTests(ChannelsLiveServerTestCase):
    serve_static = True  # emulate StaticLiveServerTestCase

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        try:
            # NOTE: Requires "chromedriver" binary to be installed in $PATH
            cls.driver = webdriver.Chrome()
        except:
            super().tearDownClass()
            raise

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def test_when_analysis_message_posted_then_seen_by_everyone_in_same_pk(self):
        try:
            self._enter_analysis_pk('11')

            self._open_new_window()
            self._enter_analysis_pk('11')

            self._switch_to_window(0)
            self._post_message('hello')
            WebDriverWait(self.driver, 2).until(lambda _:
                                                'hello' in self._analysis_log_value,
                                                'Message was not received by window 1 from window 1')
            self._switch_to_window(1)
            WebDriverWait(self.driver, 2).until(lambda _:
                                                'hello' in self._analysis_log_value,
                                                'Message was not received by window 2 from window 1')
        finally:
            self._close_all_new_windows()

    # === Utility ===

    def _enter_analysis_pk(self, pk):
        self.driver.get(self.live_server_url + '/spineyolo/images/analyze/')
        ActionChains(self.driver).send_keys(pk + '\n').perform()
        WebDriverWait(self.driver, 2).until(lambda _:
                                            pk in self.driver.current_url)

    def _open_new_window(self):
        self.driver.execute_script('window.open("about:blank", "_blank");')
        self.driver.switch_to.window(self.driver.window_handles[-1])

    def _close_all_new_windows(self):
        while len(self.driver.window_handles) > 1:
            self.driver.switch_to.window(self.driver.window_handles[-1])
            self.driver.execute_script('window.close();')
        if len(self.driver.window_handles) == 1:
            self.driver.switch_to.window(self.driver.window_handles[0])

    def _switch_to_window(self, window_index):
        self.driver.switch_to.window(self.driver.window_handles[window_index])

    def _post_message(self, message):
        ActionChains(self.driver).send_keys(message + '\n').perform()

    @property
    def _analysis_log_value(self):
        return self.driver.find_element_by_css_selector('#analysis-log').get_property('value')
