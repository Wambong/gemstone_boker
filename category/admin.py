from django.contrib import admin
# from django_mptt_admin.admin import DjangoMpttAdmin
from .models import Category
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['category_name', 'parent_category']

    def parent_category(self, obj):
        if obj.parent:
            return obj.parent.category_name
        else:
            return '-'

    parent_category.short_description = 'Parent Category'
admin.site.register(Category, CategoryAdmin)




