from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import Note


# Create your views here.
@login_required
def home(request):
    """
    Main page
    """
    notes_list = Note.objects.order_by('-pub_date')
    context = {'notes': notes_list}
    return render(request, 'notes/home.html', context)

def login_view(request):
    username =request.POST('username')
    password = request.POST('password')
    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_active:
        auth.login(request,user)
        return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('notes/login')

@login_required()
def logout_view(request):
    auth.logout(request)