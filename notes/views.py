from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import generic
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.base import View
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login

from .models import Note


# Create your views here.

class HomeView(generic.ListView):
    """
    Main page
    """
    template_name = 'notes/home.html'
    context_object_name = 'notes'

    @login_required()
    def get_queryset(self):
        return Note.objects.order_by('-pub_date')


class LoginFormView(FormView):
    form_class = AuthenticationForm

    template_name = "notes/login.html"

    success_url = "/"

    def form_valid(self, form):
        self.user = form.get_user()

        login(self.request, self.user)
        return super(LoginFormView, self).form_valid(form)


class LogoutView(View):
    @login_required()
    def get(self, request):
        logout(request)

        return HttpResponseRedirect("/")


class RegisterFormView(FormView):
    form_class = UserCreationForm

    success_url = "/notes/login/"

    template_name = "notes/register.html"

    def form_valid(self, form):
        form.save()

        return super(RegisterFormView, self).form_valid(form)
