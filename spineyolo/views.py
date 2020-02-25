from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from rest_framework.views import APIView

from spineyolo.apps import SpineyoloConfig


class CallModel(APIView):

    ## TODO: change this to POST, because need to post and wait for returns
    def get(self, request):
        if request.method == "GET":
            params = request.GET.get('scale')
            response = SpineyoloConfig.predictor
            return HttpResponse(response)


def index(request):
    return render(request, "registration/index.html")
