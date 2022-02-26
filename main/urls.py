from . import views
from django.urls import path, include

urlpatterns = [
    path('', views.index),
    path("redirect",views.move_back_home),
    path("first_html",views.first_html)
]