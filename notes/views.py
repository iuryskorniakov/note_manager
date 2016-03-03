from django.contrib.auth.decorators import login_required
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
