from django.db.models.signals import post_save
from django.dispatch import receiver
from store.models import Product
from  .utils import  send_product_notification

@receiver(post_save, sender=Product)
async def product_created(sender, instance, created, **kwargs):
    if created:
        await send_product_notification(instance)
