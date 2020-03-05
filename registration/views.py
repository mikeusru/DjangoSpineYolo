from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import CreateView, FormView

from registration.forms import SignUpForm


def index(request):
    return render(request, 'registration/index.html')


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse("django_user_logins/index.html"))


# def register(request):
#     registered = False
#     if request.method == 'POST':
#         user_form = UserForm(data=request.POST)
#         profile_form = UserProfileInfoForm(data=request.POST)
#         if user_form.is_valid() and profile_form.is_valid():
#             user = user_form.save()
#             user.set_password(user.set_password)
#             user.save()
#             profile = profile_form.save(commit=False)
#             profile.user = user
#             registered = True
#         else:
#             print(user_form.errors, profile_form.errors)
#     else:
#         user_form = UserForm()
#         profile_form = UserProfileInfoForm()
#     return render(request, 'registration/registration.html',
#                   {
#                       'user_form': user_form,
#                       'profile_form': profile_form,
#                       'registered': registered,
#                   })


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponseRedirect("Your account was inactive.")
        else:
            print("Someone tried to login and failed")
            print("They used username: {} and password:{}".format(username, password))
            return HttpResponse("Invalid login details given")
    else:
        return render(request, 'registration/login.html', {})


class RegisterView(FormView):
    form_class = SignUpForm
    template_name = 'registration/registration.html'

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data.get('username')
        raw_password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=raw_password)
        login(self.request, user)
        return redirect('index')

