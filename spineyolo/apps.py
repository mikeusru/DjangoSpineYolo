import ast
import threading
import time
from pathlib import Path

from django.apps import AppConfig

from spineyolo.prediction.SpineDetector import SpineDetector


def load_pusher_info():
    with open(Path('_private', 'pusher_keys.txt'), 'r') as pusher_inf:
        s = pusher_inf.read()
        pusher_dict = ast.literal_eval(s)
    return pusher_dict


def slow_response_function():
    time.sleep(3)
    print('slow function done')


def test_slow_responder():
    x = threading.Thread(target=slow_response_function)
    x.start()


class SpineyoloConfig(AppConfig):
    name = 'spineyolo'
    MODEL_PATH = Path("spineyolo/model")
    WEIGHTS_PATH = MODEL_PATH / Path("weights")
    STATIC_ROOT = Path("static/")
    print(MODEL_PATH.absolute())
    print(WEIGHTS_PATH.absolute())
    print(STATIC_ROOT.absolute())
    spine_detector = test_slow_responder

    # spine_detector = SpineDetector(MODEL_PATH, WEIGHTS_PATH, STATIC_ROOT)
