from django.urls import path
from . import views

urlpatterns = [
    # Main page displaying all items.
    path('', views.index, name='index'),

    # User registration page.
    path('registration/', views.registration, name='registration'),

    # Endpoint to validate user registration details.
    path('registration/validateUser', views.validateUser, name='validateUser'),

    # User login page.
    path('login/', views.log, name='log'),

    # Endpoint to authenticate user login details.
    path('login/authenticate/', views.authenticateView, name='authenticate'),
]
