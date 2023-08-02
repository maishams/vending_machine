from datetime import timezone

from django.contrib.auth.models import User
from django.db import models

class Item(models.Model):
    itemType = models.CharField('Type', choices='Mouse', max_length=25, default="Mouse")
    itemDescription = models.TextField('Description', max_length=400, help_text="Insert a brief product description",
                                       default="")
    itemPrice = models.DecimalField('Price', max_digits=4, decimal_places=2, default=0.50)
    itemQuantity = models.PositiveSmallIntegerField('Quantity', default=1, editable=True)

    def empty(self):
        Item.objects.filter(id=self.id).update(itemQuantity=0)
        Item.refresh_from_db(self)

class History(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hItemType = models.CharField('Type', choices='Mouse', max_length=25)
    hItemPrice = models.DecimalField('Price', max_digits=4, decimal_places=2, default=0.50)
    purchaseTime = models.DateTimeField('Purchase Time', default=timezone.now)

    # Method to delete a history record
    def clean(self):
        self.delete()