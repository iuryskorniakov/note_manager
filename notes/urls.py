from .views import login_view, logout_view, register_view
from django.conf.urls import url

urlpatterns = [
    url(r'^login', login_view, name='login_view'),
    url(r'logout', logout_view, name='logout_view'),
    url(r'^register', register_view, name='register_view')
]
