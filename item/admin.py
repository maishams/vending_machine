from django.contrib import admin
from .models import Item, History
from django.db.models import F

# Define an admin action to add 10 to the item quantity for selected items
def add10(modeladmin, request, queryset):
    queryset.update(itemQuantity=F('itemQuantity') + 10)
add10.short_description = "Add 10 items"

# Define an admin action to add 100 to the item quantity for selected items
def add100(modeladmin, request, queryset):
    queryset.update(itemQuantity=F('itemQuantity') + 100)
add100.short_description = "Add 100 items"

# Define an admin action to set the item quantity to 0 for selected items
def emptyitems(modeladmin, request, queryset):
    queryset.update(itemQuantity=0)
emptyitems.short_description = "Empty items"

# Define a custom admin class for the Item model
class InsertItemAdmin(admin.ModelAdmin):
    fieldsets = [
        ('EquipmentType', {'fields': ['itemType']}),
        ('EquipmentDescription', {'fields': ['itemDescription']}),
        ('EquipmentPrice', {'fields': ['itemPrice']}),
        ('EquipmentQuantity', {'fields': ['itemQuantity']}),
    ]

    # Define columns to display in the admin list view
    list_display = ('id', 'itemType', 'itemDescription', 'itemPrice', 'itemQuantity')
    # Add filters for the admin list view
    list_filter = ['itemType']
    # Add search functionality for the admin list view
    search_fields = ['itemType', 'itemDescription']
    # Add custom actions to the admin interface
    actions = [add10, add100, emptyitems]
    # Define default ordering for the admin list view
    ordering = ['id']

# Register the Item model with the custom admin class
admin.site.register(Item, InsertItemAdmin)

# Define a custom admin class for the History model
class InsertHistoryAdmin(admin.ModelAdmin):
    # Group fields in the admin form
    fieldsets = [
        ('User', {'fields': ['user']}),
        ('EquipmentType', {'fields': ['hItemType']}),
        ('EquipmentPrice', {'fields': ['hItemPrice']}),
        ('PurchaseTime', {'fields': ['purchaseTime']}),
    ]

    # Define columns to display in the admin list view
    list_display = ('user', 'hItemType', 'hItemPrice', 'purchaseTime')
    # Add filters for the admin list view
    list_filter = ['hItemType', 'purchaseTime']
    # Add search functionality for the admin list view
    search_fields = ['user', 'hItemType']
    # Define default ordering for the admin list view
    ordering = ['-purchaseTime']

# Register the History model with the custom admin class
admin.site.register(History, InsertHistoryAdmin)