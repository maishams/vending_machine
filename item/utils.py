def get_item_list_with_quantity():
    """Retrieve a list of items with their quantities."""
    return Item.objects.all().values('id', 'itemType', 'itemPrice', 'itemImage').annotate(
        itemQuantity=Sum('itemQuantity'))


def create_context_with_media_url(item_list):
    """Create a context dictionary with item list and media URL."""
    return {
        'item_list': item_list,
        'MEDIA_URL': settings.MEDIA_URL
    }


def render_index_page(request, context):
    """Render the index page with the given context."""
    return render(request, 'index.html', context)


def get_item_by_id(itemId):
    """Retrieve an item by its ID."""
    return Item.objects.filter(id=itemId).first()


def is_user_authenticated(request):
    """Check if the current user is authenticated."""
    return request.user.is_authenticated


def render_login_page(request):
    """Render the login page."""
    return render(request, 'login.html')


def item_exists(itemId):
    """Check if an item exists by its ID."""
    return Item.objects.filter(id=itemId).exists()


def get_item_and_status(itemId):
    """Retrieve an item and its status (if it's the last one)."""
    item = Item.objects.get(id=itemId)
    is_last = item.itemQuantity == 1
    return item, is_last


def try_dispense_item(item, is_last):
    """Attempt to dispense one item, considering if it's the last one."""
    return item.dispenseOneItem(is_last)


def log_purchase_history(user, item):
    """Log purchase history for a user and an item."""
    history = History(user=user, hItemType=item.itemType, hItemPrice=item.itemPrice)
    history.save()


def is_password_strong(password):
    """Check if the provided password is strong."""
    return len(password) >= 8 and any(char.isdigit() for char in password) and any(char.isalpha() for char in password)


def perform_authentication(request, details):
    """Authenticate a user with provided details."""
    return authenticate(request, username=details['username'], password=details['password'])


def log_user_in(request, user):
    """Log a user into the system."""
    login(request, user)


def get_user_history(user):
    """Get the purchase history of a user."""
    return History.objects.filter(user=user).order_by('-purchaseTime')


def delete_user_history(user):
    history_list = get_user_history(user)
    for history in history_list:
        history.clean()


def calculate_total_spending(user):
    """Calculate the total spending of a user."""
    total_spending = History.objects.filter(user=user).aggregate(total=Sum('hItemPrice')).get('total', 0)
    return round(total_spending, 2) if total_spending else 0


def determine_favourite_item_type(history_list):
    """Determine the favourite item type based on purchase history."""
    favourite_types = history_list.values("hItemType").annotate(itemQuantity=Count('hItemType'))
    return favourite_types[0]['hItemType'] if favourite_types.exists() else None


def is_staff_user(user):
    """Check if the user is a staff member."""
    return user.is_staff


def get_date_range(request):
    """Extract start and end dates from a request."""
    start_date_str = request.GET.get('start_date', None)
    end_date_str = request.GET.get('end_date', None)

    start_date = datetime.strptime(start_date_str, '%Y-%m-%d') if start_date_str else None
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d') if end_date_str else None

    return start_date, end_date


def filter_history_by_date(start_date, end_date):
    """Filter the purchase history by a date range."""
    query = History.objects.all()
    if start_date:
        query = query.filter(purchaseTime__gte=start_date)
    if end_date:
        query = query.filter(purchaseTime__lte=end_date)
    return query


def get_top_users():
    """Retrieve top users based on their spending."""
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

    return top_users
