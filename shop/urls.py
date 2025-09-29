from django.urls import path
from . import views

app_name = "shop"   

urlpatterns = [
    path("pet-services/", views.pet_services, name="pet_services"),

    # all products
    path("products/", views.all_products, name="all_products"),

    # product detail
    path("product/<slug:slug>/", views.product_detail, name="product_detail"),

    # category products
    path("<slug:main_type_slug>/<slug:category_slug>/", views.category_products, name="category_products"),

    # subcategory products
    path("<slug:main_type_slug>/<slug:category_slug>/<slug:subcategory_slug>/", views.subcategory_products, name="subcategory_products"),

    # main type products
    path("<slug:main_type_slug>/", views.main_type_products, name="main_type_products"),
]
