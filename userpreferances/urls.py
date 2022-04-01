from . import views
from django.urls import path


urlpatterns = [
    path('', views.index, name='preferences'),
    path('change-password', views.change_password, name='change-password')
]