from django.urls import path
from . import views


app_name = 'reservations'

urlpatterns = [
    path('home/', views.home, name='home'),
]
