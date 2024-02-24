from django.http import Http404
from django.shortcuts import render, redirect
from .forms import CategoryForm
from django.contrib import messages
from category.models import Category
from store.models import Product
from django.views.generic import ListView


def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'You have successfully added a new category.')
            return redirect('add_category')
    else:
        form = CategoryForm()

    return render(request, 'category/category_form.html', {'form': form})


def get_category_products(request, slug):
    categories = Category.objects.filter(slug=slug)
    if not categories.exists():
        raise Http404("Category not found")

    descendants = categories[0].get_descendants(include_self=True)

    category_products = Product.objects.filter(category__in=descendants)

    context = {
        'categories': categories[0],
        'category_products': category_products,
    }
    return render(request, 'store/store.html', context
                  )


class CategoryListView(ListView):
    model = Category
    template_name = "includes/navbar.html"
    context_object_name = 'categories'
