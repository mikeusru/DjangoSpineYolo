# SpineYolo deployment in Django

This is a django deployment of Spine Yolo, an automated deep learning model used to identify dendritic spines.

The main controller for the image analysis part is found in spineyolo/prediction/SpineDetector.py

The server requires a GPU to run this at a reasonable speed. 

The implementation includes Django Channels for asynchronous result reporting.
