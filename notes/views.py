from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.base import View
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login

from .models import Note


# Create your views here.

class HomeView(generic.DetailView):
    model = Note
    template_name = 'notes/home.html'

class ListView(generic.ListView):
    model = Note
    template_name = 'notes/list.html'


class AddNoteView(generic.CreateView):
    model = Note
    template_name = 'notes/add.html'
    success_url = '/'
    fields = ['title', 'body', 'date', 'category']

    def form_valid(self, form):
        form.instance.notes_user = self.request.user
        return super(AddNoteView, self).form_valid(form)

class DetailNoteView(generic.DetailView):
    model = Note
    template_name = 'notes/detail.html'

    def get_object(self, form):
        obj = super(DetailNoteView, self).get_object()
        return obj

class EditNoteView(generic.UpdateView):
    model = Note
    template_name = 'notes/edit.html'
    success_url = '/'
    fields = ['title', 'body', 'date', 'category']

    def get_object(self, form):
        obj = super(EditNoteView, self).get_object()
        return obj


class LoginFormView(generic.FormView):
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


class RegisterFormView(generic.FormView):
    form_class = UserCreationForm

    success_url = "notes/login/"

    template_name = "notes/register.html"

    def form_valid(self, form):
        form.save()
        return super(RegisterFormView, self).form_valid(form)
