from notes import views
from django.conf.urls import url

urlpatterns = [
    url(r'^login/$', views.LoginFormView.as_view()),
    url(r'logout/$', views.LogoutView),
    url(r'^register/$', views.RegisterFormView.as_view()),
    url(r'^home/&', views.HomeView.as_view()),
]

