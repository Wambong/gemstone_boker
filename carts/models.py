from django.db import models
from store.models import *
from accounts.models import Account, UserProfile


class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cart_id

class CartItem(models.Model):
    user = models.ForeignKey(Account, on_delete= models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete= models.CASCADE)
    variations = models.ManyToManyField(Variation, blank=True)
    cart = models.ForeignKey(Cart, on_delete= models.CASCADE, null=True)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)
    def sub_total(self):
        return self.product.price * self.quantity

    def __unicode__(self):
        return self.produt

# class Inquiry(models.Model):
#     first_name = models.CharField(max_length=100, blank=True)
#     last_name = models.CharField(max_length=100, blank=True)
#     email = models.EmailField()
#     phone = models.CharField(max_length=15)
#     seller = models.CharField(max_length=153,  null=True, blank=True)
#     country = models.CharField(max_length=153,  null=True, blank=True)
#     cart_item = models.ForeignKey(CartItem, on_delete=models.CASCADE, related_name='inquiry_cart_items')
#     inquiry_number = models.CharField(max_length=120,  default="123")
#     is_submitted = models.BooleanField(default=False)
#     inquiry_note = models.CharField(max_length=500, blank=True, null=True)
#     inquiry_date = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return f"Inquiry for {self.cart_item.product.product_name} by {self.first_name} {self.last_name}"
#
