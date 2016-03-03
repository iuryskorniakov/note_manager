from django.shortcuts import render
from .models import Note
import uuid

# Create your views here.
def home(request):
    """
    Main page
    """
    context = Note.objects.order_by('-pub_date')
    return render(request, 'notes/home.html', )