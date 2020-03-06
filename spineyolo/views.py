import json
import os
import time
from pathlib import Path

from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, DetailView
from numpy.random import rand
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
import requests

from DjangoSpineYolo.wsgi import registry
from endpoints.models import MLAlgorithm, MLRequest
from spineyolo.apps import SpineyoloConfig
from spineyolo.forms import ImageForm
from spineyolo.models import SpineData


class CallModel(APIView):

    ## TODO: change this to POST, because need to post and wait for returns
    def get(self, request):
        if request.method == "GET":
            params = request.GET.get('scale')
            response = SpineyoloConfig.predictor
            return HttpResponse(response)


class ImageListView(ListView):
    model = SpineData
    template_name = 'spineyolo/image_list.html'
    context_object_name = 'images'
    ordering = ['-date_uploaded']

    def get_queryset(self):
        queryset = super(ImageListView, self).get_queryset()
        return queryset.filter(user=self.request.user)


class AnalyzeImageView(ImageListView):
    template_name = 'spineyolo/active_analysis.html'

    def get(self, request, **kwargs):
        pk = kwargs['pk']
        object = self.get_queryset().get(pk=pk)
        # path = Path('tmp') / Path(object.image.url)
        ## TODO: Fix the way the image path is handled
        input_data = {
            "image_path": "tmp/{}".format(object.image.url),
            "scale": object.scale,
        }
        print("The special key is {}!".format(pk))
        print("The user is {}!".format(request.user))
        print("link = {}, scale = {}".format(input_data['image_path'], object.scale))
        predictor = SpineyoloConfig.spine_detector
        # predictor.set_local(True)
        # predictor.set_inputs(input_data)
        # u_id = time.strftime("%Y%m%d%H%M%S")
        # predictor.queue.put(["find_spines", u_id])
        return super(AnalyzeImageView, self).get(request)


class UploadImageView(CreateView):
    model = SpineData
    form_class = ImageForm
    # success_url = reverse_lazy('spineyolo:analyze_image')
    template_name = 'spineyolo/upload_image.html'

    def get_success_url(self):
        return reverse_lazy('spineyolo:analyze_image', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)
