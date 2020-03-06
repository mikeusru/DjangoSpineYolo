from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views.generic import FormView

from registration.forms import SignUpForm


def index(request):
    if request.user.is_authenticated:
        return redirect('spineyolo:upload_image')
    return render(request, 'index.html')


def logout_request(request):
    logout(request)
    return redirect('index')


class RegisterView(FormView):
    form_class = SignUpForm
    template_name = 'registration/registration.html'

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data.get('username')
        raw_password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=raw_password)
        login(self.request, user)
        return redirect('index')
