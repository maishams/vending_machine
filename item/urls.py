from django.urls import path
from . import views

urlpatterns = [
    # Main page displaying all items.
    path('', views.index, name='index')
]
