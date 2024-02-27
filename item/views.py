from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse

from item.utils import *


def index(request):
    """Renders the index page with a list of all items, their types, prices, and total quantity."""
    item_list = get_item_list_with_quantity()
    context = create_context_with_media_url(item_list)
    return render_index_page(request, context)


def payment(request, itemId):
    """Renders the payment page for a specific item type."""
    item = get_item_by_id(itemId)
    return render_payment_page(request, item)


def render_payment_page(request, item):
    """Renders the payment page."""
    return render(request, 'payment.html', {'item': item})


def pay(request, itemId):
    """Processes the payment for a specific item type."""
    if not is_user_authenticated(request):
        return render_login_page(request)

    if not item_exists(itemId):
        return render_error_page(request, "Item does not exist.")

    item, is_last = get_item_and_status(itemId)

    if try_dispense_item(item, is_last):
        log_purchase_history(request.user, item)
        return render_thanks_page(request)

    return render_error_page(request)


def render_thanks_page(request):
    """Renders the thanks page."""
    return render(request, 'thanksPage.html')


def render_error_page(request, error_message=None):
    """Renders the error page."""
    return render(request, 'errorPage.html', {'error_message': error_message})


def render_about_page(request):
    """Renders the about page."""
    return render(request, 'about.html')


def render_contact_page(request):
    """Renders the contact page."""
    return render(request, 'contact.html')


# Renders the registration page.
def render_registration_page(request):
    """Renders the registration page."""
    return render(request, 'registration.html')


def login_view(request, loginFailed=False):
    """Renders the login page. Displays an error message if login fails."""
    return render(request, 'login.html', {'loginFailed': loginFailed})


def render_login_error(request):
    """Renders the login page."""
    return render(request, 'login.html', {'loginFailed': True})


@login_required
def account(request):
    """Displays the user's account details including purchase history and favorite item type."""
    user = request.user
    history_list = get_user_history(user)
    total_spending = calculate_total_spending(user)
    favourite_type = determine_favourite_item_type(history_list)

    return render(request, 'account.html', {
        'user': user,
        'historyList': history_list,
        'totalSpending': total_spending,
        'favouriteType': favourite_type
    })


@login_required
def logout_view(request):
    """Logs out the authenticated user and redirects them to the index page."""
    logout(request)
    return HttpResponseRedirect(reverse('index'))


@login_required
def account(request):
    """Deletes the purchase history of the authenticated user."""
    user = request.user
    history_list = get_user_history(user)
    total_spending = calculate_total_spending(user)
    favourite_type = determine_favourite_item_type(history_list)

    context = {
        'user': user,
        'historyList': history_list,
        'totalSpending': total_spending,
        'favouriteType': favourite_type
    }

    return render(request, 'account.html', context)


@login_required
def dashboard(request):
    """Shows dashboard of trends of usage of the vending machine"""
    if not is_staff_user(request.user):
        return render_error_page(request, "Access denied.")

    start_date, end_date = get_date_range(request)
    history_query = filter_history_by_date(start_date, end_date)

    context = {
        'total_purchases': history_query.count(),
        'total_revenue': history_query.aggregate(total=Sum('hItemPrice')).get('total', 0),
        'purchases_per_item': history_query.values('hItemType').annotate(total=Count('hItemType')),
        'start_date': start_date,
        'end_date': end_date,
        'top_users': get_top_users()
    }

    return render(request, 'dashboard.html', context)


# Deletes the purchase history of the authenticated user.

@login_required
def clean_history(request):
    if not is_staff_user(request.user):
        return render_error_page(request, "You do not have permission to delete purchase history.")

    if request.method == 'POST':
        delete_user_history(request.user)
        return redirect_to_referer(request)


def redirect_to_referer(request):
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))  # Fallback to home if referer is not set.
