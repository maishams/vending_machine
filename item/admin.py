from django.contrib import admin
from .models import Item, History
from django.db.models import F


def has_permission(user):
    """
    Check if the user has the necessary permissions.
    """
    # Logic to check if user is staff
    return user.is_staff


def add10(modeladmin, request, queryset):
    """
    Admin action to increment the quantity of selected items by 10.
    """
    if has_permission(request.user):
        queryset.update(itemQuantity=F('itemQuantity') + 10)


add10.short_description = "Add 10 items"  # Description for the admin action


def add100(modeladmin, request, queryset):
    """
    Admin action to increment the quantity of selected items by 100.
    """
    if has_permission(request.user):
        queryset.update(itemQuantity=F('itemQuantity') + 100)


add100.short_description = "Add 100 items"  # Description for the admin action


def emptyitems(modeladmin, request, queryset):
    """
    Admin action to set the quantity of selected items to 0.
    """
    if has_permission(request.user):
        queryset.update(itemQuantity=0)


emptyitems.short_description = "Empty items"  # Description for the admin action


class InsertItemAdmin(admin.ModelAdmin):
    """
    Custom admin class for the Item model.
    """
    fieldsets = [
        ('EquipmentType', {'fields': ['itemType']}),
        ('EquipmentDescription', {'fields': ['itemDescription']}),
        ('EquipmentPrice', {'fields': ['itemPrice']}),
        ('EquipmentQuantity', {'fields': ['itemQuantity']}),
        ('Image', {'fields': ['itemImage']}),
    ]

    list_display = ('id', 'itemType', 'itemDescription', 'itemPrice', 'itemQuantity')  # Columns for list view
    list_filter = ['itemType']  # Filters for list view
    search_fields = ['itemType', 'itemDescription']  # Search functionality
    actions = [add10, add100, emptyitems]  # Custom actions
    ordering = ['id']  # Default ordering


# Register the Item model with the custom admin class
admin.site.register(Item, InsertItemAdmin)


class InsertHistoryAdmin(admin.ModelAdmin):
    """
    Custom admin class for the History model.
    """
    fieldsets = [
        ('User', {'fields': ['user']}),
        ('EquipmentType', {'fields': ['hItemType']}),
        ('EquipmentPrice', {'fields': ['hItemPrice']}),
        ('PurchaseTime', {'fields': ['purchaseTime']}),
    ]

    list_display = ('user', 'hItemType', 'hItemPrice', 'purchaseTime')  # Columns for list view
    list_filter = ['hItemType', 'purchaseTime']  # Filters for list view
    search_fields = ['user', 'hItemType']  # Search functionality
    ordering = ['-purchaseTime']  # Default ordering


# Register the History model with the custom admin class
admin.site.register(History, InsertHistoryAdmin)
