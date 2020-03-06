import ast
from pathlib import Path

from django.apps import AppConfig

from spineyolo.prediction.SpineDetector import SpineDetector


def load_pusher_info():
    with open(Path('_private', 'pusher_keys.txt'), 'r') as pusher_inf:
        s = pusher_inf.read()
        pusher_dict = ast.literal_eval(s)
    return pusher_dict


class SpineyoloConfig(AppConfig):
    name = 'spineyolo'
    MODEL_PATH = Path("spineyolo/model")
    WEIGHTS_PATH = MODEL_PATH / Path("weights")
    STATIC_ROOT = Path("static/")
    print(MODEL_PATH.absolute())
    print(WEIGHTS_PATH.absolute())
    print(STATIC_ROOT.absolute())
    spine_detector = 'test'
    # spine_detector = SpineDetector(MODEL_PATH, WEIGHTS_PATH, STATIC_ROOT)