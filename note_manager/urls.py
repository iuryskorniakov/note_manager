"""note_manager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin

from notes import views

urlpatterns = [
                  url(r'^$', views.main),
                  url(r'^signup$', views.signup),
                  url(r'^signin$', views.signin),
                  url(r'^signout$', views.signout),
                  url(r'^main$', views.notes_list),
                  url(r'^get_notes$',views.get_notes),
                  url(r'^get_one_note$', views.get_one_note),
                  url(r'^note/(?P<uu_id>.*)$',views.view_note),
                  url(r'^add_note$', views.add_note),
                  url(r'^edit_note$', views.edit_note),
                  url(r'^delete_note$', views.delete_note),
                  url(r'^admin/', include(admin.site.urls)),
                  url(r'^get_categories$', views.get_category)
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
