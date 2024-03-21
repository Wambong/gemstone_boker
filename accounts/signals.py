from django.db.models.signals import post_save
from django.dispatch import receiver
from store.models import Product, ReviewRating
from  .utils import  send_notification

@receiver(post_save, sender=Product)
def product_created(sender, instance, created, **kwargs):
    if created:
        message = f"New product added: {instance.product_name}\nPrice: {instance.price}\nBy: {instance.seller}"
        send_notification(message)


