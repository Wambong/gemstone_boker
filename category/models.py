from django.db import models
from django.utils.text import slugify
from django.urls import reverse


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
        indent = '--' * self.level()
        return f'{indent}{self.category_name}'

    def level(self):
        level = 0
        instance = self
        while instance.parent:
            level += 1
            instance = instance.parent
        return level


    def save(self, *args, **kwargs):
        if self.slug is None:
            slug = slugify(self.category_name)
            has_slug = Category.objects.filter(slug=slug).exists()
            count = 1
            while has_slug:
                count += 1
                slug = slugify(self.category_name) + '-' + str(count)
                has_slug = Category.objects.filter(slug=slug).exists()
            self.slug = slug
        super().save(*args, **kwargs)

