from django.shortcuts import render, get_object_or_404,  redirect
from .models import MainType, Category, SubCategory, Product, Brand, Breed, TopDeal, Review 
from django.core.paginator import Paginator
from home.models import SiteSettings
from django.db.models import Avg, Count
from django.db import models
from .forms import ReviewForm



from django.contrib import messages  # make sure this is imported

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)

    reviews = product.reviews.all()
    avg_rating = reviews.aggregate(Avg("rating"))["rating__avg"] or 0
    review_count = reviews.count()

    # Rating breakdown
    rating_breakdown = reviews.values("rating").annotate(count=Count("id"))
    breakdown_dict = {i: 0 for i in range(1, 6)}
    for rb in rating_breakdown:
        breakdown_dict[rb["rating"]] = rb["count"]

    breakdown_percent = {
        i: (breakdown_dict[i] / review_count * 100) if review_count > 0 else 0
        for i in range(1, 6)
    }

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.save()
            messages.success(request, "✅ Your review has been submitted successfully!")
            return redirect("shop:product_detail", slug=product.slug)  # redirect with message
    else:
        form = ReviewForm()

    context = {
        "product": product,
        "reviews": reviews,
        "avg_rating": avg_rating,
        "review_count": review_count,
        "breakdown": breakdown_dict,
        "breakdown_percent": breakdown_percent,
        "form": form,
    }
    return render(request, "shop/product_detail.html", context)


from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Avg, Count
from django.core.paginator import Paginator
from .models import MainType, Category, SubCategory, Product, Brand, Breed, TopDeal, Review


from django.shortcuts import render, get_object_or_404
from .models import MainType, Product, Category, SubCategory

def main_type_products(request, main_type_slug):
    # Fetch the main type (dog, cat, etc.)
    main_type = get_object_or_404(MainType, slug=main_type_slug)

    # Base queryset
    products = Product.objects.filter(main_type=main_type, is_available=True)

  # Filters
    brands = Brand.objects.all()
    breeds = Breed.objects.filter(main_type=main_type)
    product_sizes = Product.SIZE_CHOICES
    product_life_stages = Product.LIFE_STAGE_CHOICES


    # Optional category/subcategory filtering
    category_slug = request.GET.get("category")
    subcategory_slug = request.GET.get("subcategory")

    category = None
    subcategory = None

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug, main_type=main_type)
        products = products.filter(category=category)

    if subcategory_slug:
        subcategory = get_object_or_404(SubCategory, slug=subcategory_slug, category__main_type=main_type)
        products = products.filter(subcategory=subcategory)

    # Sorting
    sort_by = request.GET.get("sort")
    if sort_by == "price_low_high":
        products = products.order_by("price")
    elif sort_by == "price_high_low":
        products = products.order_by("-price")
    elif sort_by == "rating":
        products = products.order_by("-avg_rating")
    elif sort_by == "newest":
        products = products.order_by("-created_at")
    # ✅ Load top deals for this main_type
    top_deals = TopDeal.objects.filter(main_type=main_type)
    context = {
        "main_type": main_type,
        "selected_main_type": main_type, 
        "category": category,
        "subcategory": subcategory,
        "products": products,
        "top_deals": top_deals,
        "brands": brands,
        "breeds": breeds,
        "product_sizes": product_sizes,
        "product_life_stages": product_life_stages,
    }
    return render(request, "shop/main_type_products.html", context)


def category_products(request, main_type_slug, category_slug):
    """Redirect to main_type_products with category filter applied"""
    return redirect(f"/shop/{main_type_slug}/?category={category_slug}")


def subcategory_products(request, main_type_slug, category_slug, subcategory_slug):
    """Redirect to main_type_products with category + subcategory filter"""
    return redirect(f"/shop/{main_type_slug}/?category={category_slug}&subcategory={subcategory_slug}")

 

def pet_services(request):
    settings = SiteSettings.objects.first()  # fetch logo etc.
    return render(request, "shop/pet_services.html", {
        "settings": settings,
        'selected_main_type': MainType.objects.get(slug="pet-services"),
    })



from django.shortcuts import render
from .models import Product

from types import SimpleNamespace

def all_products(request):
    products = Product.objects.all().order_by("-id")  
    main_type = SimpleNamespace(name="All Products", slug="products")

    return render(request, "shop/main_type_products.html", {
        "products": products,
        "main_type": main_type,  
        "category": None,
        "subcategory": None,
        "top_deals": [],
        "page_obj": products,
    })

