from django.shortcuts import render
from store.models import Product, ReviewRating, Tag
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from accounts.models import Testimony
from category.models import Category

def home(request):
    productss = Product.objects.all().filter(is_Available=True).order_by('created_date')
    testimonies = Testimony.objects.filter(approved=True).order_by('-created_at')
    tags = Tag.objects.all()
    countries = [country[0] for country in Product.COUNTRY]
    # Filtering based on selected tags
    selected_tags = request.GET.getlist('tag')
    if selected_tags:
        productss = productss.filter(tags__name__in=selected_tags).distinct()

    # Filtering based on selected country
    selected_country = request.GET.getlist('country')
    if selected_country:
        productss = productss.filter(country__in=selected_country)

    paginator = Paginator(productss , 16)
    page_number = request.GET.get('page')
    try:
        products = paginator.page(page_number)

    except PageNotAnInteger:
        products = paginator.page(1)

    except EmptyPage:
        products = paginator.page(paginator.num_pages)



    reviews = None
    for product in productss:
        reviews = ReviewRating.objects.filter(product_id=product.id, status=True)


    context= {
    "testimonies":testimonies,
    'products': products,
    'reviews':reviews,
        'tags': tags,
        'countries': countries,

    }
    return render(request, 'home.html', context)
