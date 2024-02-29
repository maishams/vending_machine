from django.urls import path
from . import views
from . import forms

urlpatterns = [
    # Main page displaying all items.
    path('', views.index, name='index'),

    # Payment page for a specific item type.
    path('<int:item_id>/payment/', views.payment, name='payment'),

    # Endpoint to process payment for a specific item type.
    path('<int:item_id>/payment/pay/', views.pay, name='pay'),

    # About page of the website.
    path('about/', views.render_about_page, name='about'),

    # Contact page of the website.
    path('contact/', views.render_contact_page, name='contact'),

    # User registration page.
    path('registration/', views.render_registration_page, name='registration'),

    # Endpoint to validate user registration details.
    path('registration/validateUser', forms.validate_registration_details, name='validateUser'),

    # User login page.
    path('login/', views.login_view, name='log'),

    # Endpoint to authenticate user login details.
    path('login/authenticate/', forms.authenticate_user, name='authenticate'),

    # Endpoint to log out the authenticated user.
    path('logout/', views.logout_view, name='logout'),

    # User account page displaying purchase history and other details.
    path('account/', views.account, name='account'),

    # Endpoint to clear the user's purchase history.
    path('account/clean', views.clean_history, name='cleanHistory'),
]
