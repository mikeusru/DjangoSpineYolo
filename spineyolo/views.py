import json

from django.forms import formset_factory
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from spineyolo.apps import SpineyoloConfig
from spineyolo.forms import ImageForm, RatingFormSet
from spineyolo.models import SpineData, toggle_rating


def run_spineyolo(input_data, pk):
    spine_detector = SpineyoloConfig.spine_detector
    spine_detector.set_front_end_pk(pk)
    spine_detector.set_inputs(input_data)
    ## TODO: uid was put in the queue before. this may work better to avoid errors... we'll see. ok maybe it should report both pk and username so it's only showing the latest info.
    spine_detector.queue.put(["find_spines", pk])


def change_rating(request):
    if request.method == 'POST':
        print("WE GOT SOMEWHERE")
        pk = request.POST.get('pk')
        print(pk)
        rating = toggle_rating(pk)
        return HttpResponse(json.dumps({'rating': rating,
                                        'pk': pk}),
                            content_type="application/json")


class ImageListView(ListView):
    model = SpineData
    template_name = 'spineyolo/image_list.html'
    context_object_name = 'images'
    ordering = ['-date_uploaded']
    # form_class = RatingFormSet

    # def get_context_data(self, **kwargs):
    #     data = super(ImageListView, self).get_context_data(**kwargs)
    #     if self.request.POST:
    #         print("POST")
    #     else:
    #         print("NOT A POST")
    #         data['ratings'] = RatingFormSet()
    #     return data

    def get_queryset(self):
        queryset = super(ImageListView, self).get_queryset()
        return queryset.filter(user=self.request.user)


class AnalyzeImageView(ImageListView):
    template_name = 'spineyolo/active_analysis.html'

    def get(self, request, **kwargs):
        pk = kwargs['pk']
        obj = self.get_queryset().get(pk=pk)
        ## TODO: Fix the way the image path is handled
        input_data = {
            "image_path": "tmp/{}".format(obj.image.url),
            "scale": obj.scale,
        }
        run_spineyolo(input_data, pk)
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        context['pk'] = pk  # pk is in the template now
        return self.render_to_response(context)


class UploadImageView(CreateView):
    model = SpineData
    form_class = ImageForm
    template_name = 'spineyolo/upload_image.html'

    def get_success_url(self):
        return reverse_lazy('spineyolo:analyze_image', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)
