from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import generic
from django.views.generic.edit import FormView, CreateView, UpdateView
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.base import View
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login

from .models import Note


# Create your views here.

class HomeView(generic.DetailView):
    """
    Main page
    """
    model = Note
    template_name = 'notes/home.html'


class AddNotes(generic.CreateView):
    model = Note
    template_name = 'notes/add.html'
    success_url = '/'
    fields = ['title', 'body', 'date', 'category']

    def form_valid(self, form):
        form.instance.notes_user = self.request.user
        return super(AddNotes, self).form_valid(form)

class DetailNotes(generic.DetailView):
    model = Note
    template_name = 'notes/detail.html'

    @property
    def get_object(self):
        obj = super(DetailNotes, self).get_object
        return obj

class EditNotes(UpdateView):
    model = Note
    template_name = 'notes/edit.html'
    success_url = '/'
    fields = ['title', 'body', 'date', 'category']

    def get_object(self):
        obj = super(EditNotes, self).get_object
        return obj


class LoginFormView(FormView):
    form_class = AuthenticationForm

    template_name = "notes/login.html"

    success_url = "/"

    def form_valid(self, form):
        self.user = form.get_user()

        login(self.request, self.user)
        return super(LoginFormView, self).form_valid(form)


@login_required()
def LogoutView(request):
    logout(request)
    return HttpResponseRedirect("/")


class RegisterFormView(FormView):
    form_class = UserCreationForm

    success_url = "/notes/login/"

    template_name = "notes/register.html"

    def form_valid(self, form):
        form.save()
        return super(RegisterFormView, self).form_valid(form)
