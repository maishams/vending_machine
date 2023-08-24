from datetime import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Sum, Count
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from VendingMachine import settings
from .models import Item, History


# Renders the index page with a list of all items, their types, prices, and total quantity.
def index(request):
    item_list = Item.objects.all().values('id', 'itemType', 'itemPrice', 'itemImage').annotate(
        itemQuantity=Sum('itemQuantity'))
    context = {
        'item_list': item_list,
        'MEDIA_URL': settings.MEDIA_URL
    }
    return render(request, 'index.html', context)


# Renders the payment page for a specific item type.
def payment(request, itemId):
    item = Item.objects.filter(id=itemId).first()
    return render(request, 'payment.html', {'item': item})


# Processes the payment for a specific item type.
def pay(request, itemId):
    # Check if user is authenticated
    if not request.user.is_authenticated:
        return render(request, 'login.html')

    # Check if the item exists
    item_exists = Item.objects.filter(id=itemId).exists()

    if not item_exists:
        return render(request, 'errorPage.html', {'error_message': "Item does not exist."})

    # Fetch the item and determine if it's the last one
    item = Item.objects.get(id=itemId)
    isLast = item.itemQuantity == 1

    # Try to delete one item
    if item.dispenseOneItem(isLast):
        # Log the purchase in the history
        history = History(user=request.user, hItemType=item.itemType, hItemPrice=item.itemPrice)
        history.save()

        return render(request, 'thanksPage.html')

    # Handle the case where the item couldn't be deleted, e.g., redirect to an error page or try again
    return render(request, 'errorPage.html')


# Renders the about page.
def about(request):
    return render(request, 'about.html')


# Renders the contact page.
def contact(request):
    return render(request, 'contact.html')


# Renders the registration page.
def registration(request):
    return render(request, 'registration.html')


# Validates user registration by checking if the username already exists and if the passwords match.
def validateRegistrationDetails(request):
    context = {'registrationFailed': False}

    if request.method == 'POST':
        username = request.POST.get('user')
        name = request.POST.get('name')
        lastName = request.POST.get('last_name')
        password = request.POST.get('password')
        confirm = request.POST.get('confirm_password')

        # Check if user already exists
        if User.objects.filter(username=username).exists():
            context['registrationFailed'] = True
            context['error_message'] = "Username already exists."
        # Check if passwords match
        elif password != confirm:
            context['registrationFailed'] = True
            context['error_message'] = "Passwords do not match."
        # Check password strength
        elif len(password) < 8 or not any(char.isdigit() for char in password) or not any(
                char.isalpha() for char in password):
            context['registrationFailed'] = True
            context[
                'error_message'] = "Password must be at least 8 characters long and contain both numbers and letters."
        else:
            user = User(username=username, first_name=name, last_name=lastName)
            user.set_password(password)
            user.save()
            return HttpResponseRedirect(reverse(loginView))

    return render(request, 'registration.html', context)


# Renders the login page. Displays an error message if login fails.
def loginView(request, loginFailed=False):
    return render(request, 'login.html', {'loginFailed': loginFailed})


# Authenticates user credentials and logs them in if valid.
def authenticateUser(request):
    if request.method == 'POST':
        username = request.POST.get('user')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        # If user is authenticated, log them in and redirect to index.
        if user:
            loginView(request, user)
            return HttpResponseRedirect(reverse('index'))

        # If authentication fails, render the login page with an error message.
        return render(request, 'login.html', {'loginFailed': True})


# Displays the user's account details including purchase history and favorite item type.
@login_required
def account(request):
    user = request.user
    historyList = History.objects.filter(user=user).order_by('-purchaseTime')

    # Calculate the total spending of the user.
    totalSpending = History.objects.filter(user=user).aggregate(total=Sum('hItemPrice')).get('total', 0)
    totalSpending = round(totalSpending, 2) if totalSpending else 0

    # Determine the user's favorite item type based on purchase history.
    favourite_types = historyList.values("hItemType").annotate(itemQuantity=Count('hItemType'))
    favouriteType = favourite_types[0]['hItemType'] if favourite_types.exists() else None

    # Render the account page with the user's details.
    return render(request, 'account.html',
                  {'user': user, 'historyList': historyList, 'totalSpending': totalSpending,
                   'favouriteType': favouriteType})

# Logs out the authenticated user and redirects them to the index page.
@login_required
def logoutView(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


# Deletes the purchase history of the authenticated user.
@login_required
def cleanHistory(request):
    if request.user.is_staff:
        user = request.user
        # If the request method is POST, it means the user has confirmed the deletion.
        if request.method == 'POST':
            # Fetch all history records associated with the user.
            historyList = History.objects.filter(user=user)

            # Delete each history record.
            for history in historyList:
                history.clean()

            # Redirect the user to the previous page they were on.
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            return render(request, 'errorPage.html',
                          {'error_message': "You do not have permission to delete purchase history."})


# Shows dashboard of trends of usage of the vending machine
@login_required
def dashboard(request):
    if not request.user.is_staff:
        # Restrict access if the user is not an admin
        return render(request, 'errorPage.html', {'error_message': "Access denied."})

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
