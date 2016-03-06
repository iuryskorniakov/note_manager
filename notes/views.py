from datetime import datetime
import json
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login
from django.http import JsonResponse, Http404
from django.shortcuts import render, redirect

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.db.models import Q
from .models import Notes, Category


# Create your views here


def main(request):
    """
    Renders start page
    """
    if request.user.is_authenticated():
        return redirect('/main')
    return render(request, 'notes/login.html')


def signup(request):
    """
    Site registration function
    """
    my_email = request.POST.get('email', "")
    my_password = request.POST.get('password', "")
    my_pass_conf = request.POST.get('confirm', "")

    if User.objects.filter(username=my_email).count():
        return JsonResponse({'success': False, 'error': 'error'})
    if not my_email:
        return JsonResponse({'success': False, 'error': 'error'})
    if not my_password:
        return JsonResponse({'success': False, 'error': 'error'})
    if my_password != my_pass_conf:
        return JsonResponse({'success': False, 'error': 'error'})

    user = User.objects.create_user(username=my_email, email=my_email)
    user.set_password(my_password)
    user.save()
    user.backend = "django.contrib.auth.backends.ModelBackend"
    auth_login(request, user)
    return JsonResponse({'success': True})


def signin(request):
    """
    Site log in function
    """
    my_email = request.POST.get('email', "")
    my_password = request.POST.get('password', "")

    try:
        user = User.objects.get(email__iexact=my_email, is_active=True)
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'error'})

    if not user.check_password(my_password):
        return JsonResponse({'success': False, 'error': 'error'})
    user.backend = "django.contrib.auth.backends.ModelBackend"
    auth_login(request, user)
    return JsonResponse({'success': True})


@login_required
def signout(request):
    """
    Site logout function
    :type request: object
    """
    if request.user.is_authenticated():
        auth.logout(request)
        return redirect('/')


def notes_list(request):
    """
    :type request: object
    :param request:
    """
    if not request.user.is_authenticated():
        return redirect('/')
    user = request.user
    data = {
        'user': user.username
    }
    return render(request, "notes/main.html", data)


def get_notes(request):
    row = []
    u_notes = Notes.objects.filter(user=request.user)
    filters = json.loads(request.POST.get('filter', '{}'))
    if len(filters):
        for filter_ in filters:
            filter_value = filter_['value']
            if filter_['field'] == 'title':
                u_notes = u_notes.filter(title__icontains=filter_value)
            if filter_['field'] == 'favorites':
                u_notes = u_notes.filter(favorites=filter_value)
            if filter_['field'] == 'category':
                query = Q()
                for cat in filter_value:
                    query = query | Q(category=cat)
                u_notes = u_notes.filter(query)
            if filter_['field'] == 'date_time':
                filter_value = datetime.strptime(filter_value, '%m/%d/%Y')
                if filter_['comparison'] == 'eq':
                    filter_range = (
                        datetime.combine(filter_value, datetime.min.time()),
                        datetime.combine(filter_value, datetime.max.time())
                    )
                if filter_['comparison'] == 'lt':
                    filter_range = (
                        datetime.strptime('01/01/2000', '%m/%d/%Y'),
                        datetime.combine(filter_value, datetime.min.time())
                    )
                if filter_['comparison'] == 'gt':
                    filter_range = (
                        datetime.combine(filter_value, datetime.max.time()),
                        datetime.strptime('01/01/2100', '%m/%d/%Y')
                    )
                u_notes = u_notes.filter(date_time__range=filter_range)
    for obj in u_notes:
        row.append({'title': obj.title,
                    'category': obj.category,
                    'text': obj.text,
                    'favorites': obj.favorites,
                    'uuid': obj.uu_id,
                    'date_time': obj.date_time,
                    'publish': obj.publish})
    return JsonResponse({'row': row})


def get_one_note(request):
    uu_id = request.POST.get('uuid', '')
    try:
        note = Notes.objects.get(uu_id=uu_id)
    except Notes.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'does_not_exist'})
    data = {'title': note.title,
            'category': note.category,
            'text': note.text,
            'favorites': note.favorites,
            'publish': note.publish,
            'uuid': note.uu_id}
    return JsonResponse({'success': True, 'data': data})


def get_category(request):
    categories = []
    for obj in Category.objects.all():
        categories.append(obj)
    return JsonResponse({'categories': categories})


def view_note(request, uu_id):
    try:
        note = Notes.objects.get(uu_id=uu_id)
    except Notes.DoesNotExist:
        raise Http404
    data = {'title': note.title,
            'category': note.category,
            'text': note.text,
            'favorites': note.favorites,
            'uuid': note.uu_id,
            'publish': note.publish,
            'date_time': note.date_time}
    if (not data['publish']) and (request.user != note.user):
        raise Http404
    return render(request, 'notes/note.html', data)


def add_note(request):
    title = request.POST.get('title', '')
    category = request.POST.get('category', 'Notice')
    text = request.POST.get('text', 'Nothing to say...')
    favorites = request.POST.get('favorites', False)
    publish = request.POST.get('publish', False)
    try:
        Notes.objects.create(user=request.user,
                             title=title,
                             category=category,
                             text=text,
                             favorites=favorites,
                             publish=publish)
    except ValueError:
        return JsonResponse({'success': False})
    return JsonResponse({'success': True})


def edit_note(request):
    uu_id = request.POST.get('uuid', '')
    title = request.POST.get('title', '')
    category = request.POST.get('category', 'Notice')
    text = request.POST.get('text', 'Nothing to say...')
    favorites = request.POST.get('favorites', False)
    publish = request.POST.get('publish', False)
    date_time = datetime.now()
    try:
        Notes.objects.filter(uu_id=uu_id).update(title=title,
                                                 category=category,
                                                 text=text,
                                                 favorites=favorites,
                                                 publish=publish,
                                                 date_time=date_time)
    except Notes.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'does_not_exist'})
    return JsonResponse({'success': True})


def delete_note(request):
    uu_id = request.POST.get('uuid', '')
    try:
        Notes.objects.filter(uu_id=uu_id).delete()
    except Notes.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'does_not_exist'})
    return JsonResponse({'success': True})