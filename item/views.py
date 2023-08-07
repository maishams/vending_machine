from datetime import datetime

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Sum, Count
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Item, History


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

# Shows dashboard of trends of usage of the vending machine
@login_required
def dashboard(request):
    # Fetch start and end dates from the request
    start_date_str = request.GET.get('start_date', None)
    end_date_str = request.GET.get('end_date', None)

    # Convert string dates to datetime objects
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d') if start_date_str else None
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d') if end_date_str else None

    # Filter the History based on the provided dates
    history_query = History.objects.all()
    if start_date:
        history_query = history_query.filter(purchaseTime__gte=start_date)
    if end_date:
        history_query = history_query.filter(purchaseTime__lte=end_date)

    # Fetch and aggregate user activity data
    total_purchases = history_query.count()
    total_revenue = history_query.aggregate(total=Sum('hItemPrice')).get('total', 0)
    purchases_per_item = history_query.values('hItemType').annotate(total=Count('hItemType'))

    context = {
        'total_purchases': total_purchases,
        'total_revenue': total_revenue,
        'purchases_per_item': purchases_per_item,
        'start_date': start_date,
        'end_date': end_date
    }

    # Fetch the count of each itemDescription bought
    purchases_per_description = History.objects.values('hItemType').annotate(total=Count('hItemType'))
    for purchase in purchases_per_description:
        item_description = Item.objects.filter(itemType=purchase['hItemType']).first().itemDescription
        purchase['itemDescription'] = item_description

        # Fetch the top 10 users who have bought items
        top_users_data = History.objects.values('user_id').annotate(
            total_spent=Sum('hItemPrice'),
            items_bought=Count('hItemType')
        ).order_by('-total_spent')[:10]

        top_users = []
        for user_data in top_users_data:
            user = User.objects.get(id=user_data['user_id'])
            top_users.append({
                'username': user.username,
                'total_spent': user_data['total_spent'],
                'items_bought': user_data['items_bought']
            })

        context.update({
            'purchases_per_description': purchases_per_description,
            'top_users': top_users
        })

        return render(request, 'dashboard.html', context)
