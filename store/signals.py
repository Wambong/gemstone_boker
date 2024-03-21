from django.db.models.signals import post_save
from django.dispatch import receiver
from store.models import Product, ReviewRating
from accounts.utils import send_notification

@receiver(post_save, sender=ReviewRating)
def comment_created(sender, instance, created, **kwargs):
    if created:
        message = f"New comment on: {instance.product.product_name}\nRating: {instance.rating}"
        send_notification(message)
