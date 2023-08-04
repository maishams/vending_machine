from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.db.models import Sum
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Item


# Renders the index page with a list of all items, their types, prices, and total quantity.
def index(request):
    item_list = Item.objects.all().values('id', 'itemType', 'itemPrice').annotate(
        itemQuantity=Sum('itemQuantity'))
    return render(request, 'index.html')

# Renders the login page. Displays an error message if login fails.
def log(request, loginFailed=False):
    return render(request, 'login.html', {'loginFailed': loginFailed})

# Authenticates user credentials and logs them in if valid.
def authenticateView(request):
    if request.method == 'POST':
        username = request.POST.get('user')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        # If user is authenticated, log them in and redirect to index.
        if user:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))

        # If authentication fails, render the login page with an error message.
        return render(request, 'login.html', {'loginFailed': True})