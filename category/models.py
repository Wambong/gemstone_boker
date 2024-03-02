from django.db import models
from django.utils.text import slugify
from django.urls import reverse
# from mptt.models import MPTTModel, TreeForeignKey


#
# class Category(MPTTModel):
#     category_name = models.CharField(max_length=50, unique=True)
#     parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children', )
#     slug = models.SlugField(max_length=100, unique=True)
#
#     class MPTTMeta:
#         order_insertion_by = ['category_name',]
#
#     class Meta:
#         unique_together = [['parent', 'slug', ]]
#         verbose_name = 'category'
#         verbose_name_plural = 'categories'
#
#     def get_url(self):
#         return reverse('products_by_category', args=[self.slug])
#
#     def __str__(self):
#         return f'{self.category_name} , {self.parent}'




class Category(models.Model):
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    category_name = models.CharField(max_length=220, unique=True)
    slug = models.SlugField(max_length=200, unique=True)


    class Meta:
        unique_together = [['parent', 'slug', ]]
        verbose_name = 'category'
        verbose_name_plural = 'categories'


    def get_absolute_url(self):
        return '/%s/' % (self.slug)

    def __str__(self):
        return f'{self.category_name}'

    def save(self, *args, **kwargs):

        if self.slug == None:
            slug = slugify(self.category_name)

            has_slug = Category.objects.filter(slug=slug).exists()
            count = 1
            while has_slug:
                count += 1
                slug = slugify(self.category_name) + '-' + str(count)
                has_slug = Category.objects.filter(slug=slug).exists()

            self.slug = slug

        super().save(*args, **kwargs)