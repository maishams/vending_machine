from django.db.models import Sum
from django.shortcuts import render

from .models import Item


# Renders the index page with a list of all items, their types, prices, and total quantity.
def index(request):
    item_list = Item.objects.all().values('id', 'itemType', 'itemPrice').annotate(
        itemQuantity=Sum('itemQuantity'))
    return render(request, 'index.html')