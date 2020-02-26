from django.test import TestCase

from rest_framework.test import APIClient


class EndpointTests(TestCase):

    def test_predict_view(self):
        client = APIClient()
        input_data = {
            "scale": 15,
            "image_path": "static/tests/test_spines.jpg",
            }
        classifier_url = "/api/v1/spine_finder/predict"
        response = client.post(classifier_url, input_data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(1 < len(response.data['prediction']) < 10)
        self.assertTrue("request_id" in response.data)
