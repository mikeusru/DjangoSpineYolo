"""
WSGI config for DjangoSpineYolo project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os
from pathlib import Path

from django.core.wsgi import get_wsgi_application

from spineyolo.prediction.SpineDetector import SpineDetector
from spineyolo.registry import MLRegistry

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoSpineYolo.settings')

application = get_wsgi_application()

MODEL_PATH = Path("spineyolo/model")
WEIGHTS_PATH = MODEL_PATH / Path("weights")
STATIC_ROOT = Path("static/")

try:
    registry = MLRegistry()  # create ML registry
    # SpineYolo
    sy = SpineDetector(MODEL_PATH, WEIGHTS_PATH, STATIC_ROOT)
    # add to ML registry
    registry.add_algorithm(endpoint_name="spine_finder",
                           algorithm_object=sy,
                           algorithm_name="spineyolo",
                           algorithm_status="production",
                           algorithm_version="0.0.1",
                           owner="Misha",
                           algorithm_description="Yolov3 specifically for dendritic spine images",
                           algorithm_path="spineyolo/model/model.json")

except Exception as e:
    print("Exception while loading the algorithms to the registry,", str(e))
