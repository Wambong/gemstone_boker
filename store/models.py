from django.db import models
from django.shortcuts import render
from django.utils.text import slugify
# from ckeditor_uploader.fields import RichTextUploadingField

from category.models import Category
from django.urls import reverse
from accounts.models import Account
from django.db.models import Avg, Count
from django_ckeditor_5.fields import CKEditor5Field

class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    COUNTRY = (
        ('Algeria', 'Algeria'), ('Angola', 'Angola'), ('Benin', 'Benin'), ('Botswana', 'Botswana'),
        ('Burkina Faso', 'Burkina Faso'),
        ('Burundi', 'Burundi'), ('Cape Verde', 'Cape Verde'), ('Central African Republic', 'Central African Republic'),
        ('Chad', 'Chad'), ('Comoros', 'Comoros'),
        ('Cameroon', 'Cameroon'), ('Congo', 'Congo'), ("Cote D'Ivoire", "Cote D'Ivoire"), ('Djibouti', 'Djibouti'),
        ('DR. Congo', 'DR. Congo'),
        ('Egypt', 'Egypt'), ('Equatorial Guinea', 'Equatorial Guinea'), ('Eritrea', 'Eritrea'),
        ('Ethiopia', 'Ethiopia'), ('Gabon', 'Gabon'),
        ('Gambia', 'Gambia'), ('Ghana', 'Ghana'), ('Guinea', 'Guinea'), ('Guinea-Bissau', 'Guinea-Bissau'),
        ('Kenya', 'Kenya'),
        ('Lesotho', 'Lesotho'), ('Liberia', 'Liberia'), ('Libya', 'Libya'), ('Madagascar', 'Madagascar'),
        ('Malawi', 'Malawi'), ('Mali', 'Mali'),
        ('Mauritania', 'Mauritania'), ('Mauritius', 'Mauritius'), ('Morocco', 'Morocco'), ('Mozambique', 'Mozambique'),
        ('Namibia', 'Namibia'), ('Niger', 'Niger'), ('Nigeria', 'Nigeria'), ('Rwanda', 'Rwanda'),
        ('Senegal', 'Senegal'), ('Seychelles', 'Seychelles'), ('Sierra Leone', 'Sierra Leone'), ('Somalia', 'Somalia'),
        ('South Africa', 'South Africa'), ('South Sudan', 'South Sudan'), ('Sudan', 'Sudan'),
        ('Swaziland', 'Swaziland'),
        ('Togo', 'Togo'), ('Tunisia', 'Tunisia'), ('Uganda', 'Uganda'), ('Zambia', 'Zambia'), ('Zimbabwe', 'Zimbabwe'),
    )
    product_name = models.CharField(max_length=200, unique=True)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE, null=True, blank=True)
    parent = models.ForeignKey('self', related_name='variants', on_delete=models.CASCADE, blank=True, null=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = CKEditor5Field('Text', config_name='extends', null=True, blank=True)
    seller = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, blank=True)
    price = models.IntegerField()
    images = models.ImageField(upload_to='photos/products')
    stock = models.IntegerField()
    country = models.CharField(max_length=220, choices=COUNTRY, null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True, null= True)
    is_Available = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
    modified_date = models.DateTimeField(auto_now=True)

    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])

    def __str__(self):
        return self.product_name

    def averageReview(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(average=Avg('rating'))
        avg = 0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
        return avg

    def countReview(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(count=Count('id'))
        count = 0
        if reviews['count'] is not None:
            count = int(reviews['count'])
        return count

    def save(self, *args, **kwargs):

        if self.slug == None:
            slug = slugify(self.product_name)

            has_slug = Product.objects.filter(slug=slug).exists()
            count = 1
            while has_slug:
                count += 1
                slug = slugify(self.product_name) + '-' + str(count)
                has_slug = Product.objects.filter(slug=slug).exists()

            self.slug = slug

        super().save(*args, **kwargs)


class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager, self).filter(variation_category='color', is_active=True)

    def sizes(self):
        return super(VariationManager, self).filter(variation_category='size', is_active=True)


variation_category_choice = (
    ('color', 'color'),
    ('size', 'size'),
)


class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=100, choices=variation_category_choice)
    variation_value = models.CharField(max_length=100, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now=True)

    objects = VariationManager()

    def __str__(self):
        return self.variation_value


class ReviewRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, blank=True)
    review = models.TextField(max_length=500, blank=True)
    rating = models.FloatField()
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject


class ProductGallery(models.Model):
    product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='store/products', max_length=255)

    def __str__(self):
        return self.product.product_name

    class Meta:
        verbose_name = 'productgallery'
        verbose_name_plural = 'product gallery'
