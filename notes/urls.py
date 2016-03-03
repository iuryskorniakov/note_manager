from notes import views
from django.conf.urls import url

urlpatterns = [
    url(r'^login/$', views.LoginFormView.as_view(), name='login'),
    url(r'^logout/$', views.LogoutView, name='logout'),
    url(r'^register/$', views.RegisterFormView.as_view()),
    url(r'^add/&', views.AddNoteView.as_view()),
    url(r'^edit/&', views.EditNoteView.as_view()),
    url(r'^detail/&', views.DetailNoteView.as_view()),
    url(r'^home/&', views.HomeView.as_view()),
]

