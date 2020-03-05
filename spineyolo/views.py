from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from rest_framework.views import APIView

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


def index(request):
    return render(request, "registration/index.html")


class ImageListView(ListView):
    model = SpineData
    template_name = 'spineyolo/class_image_list.html'
    context_object_name = 'images'


class UploadImageView(CreateView):
    model = SpineData
    form_class = ImageForm
    success_url = reverse_lazy('class_image_list')
    template_name = 'spineyolo/upload_image.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)
