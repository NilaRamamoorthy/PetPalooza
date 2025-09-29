from django.contrib import admin
from .models import (
    MainType,
    Category,
    SubCategory,
    Brand,
    Breed,
    Product,
    ProductImage,
    TopDeal,
   Review,
)

admin.site.register(Review)



# ---------------------------
# Inline for Product Images
# ---------------------------
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


# ---------------------------
# Product Admin
# ---------------------------
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'main_type', 'category', 'subcategory', 'brand', 'price', 'is_available')
    list_filter = ('main_type', 'category', 'subcategory', 'brand', 'breed', 'is_available')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline]


# ---------------------------
# SubCategory Admin
# ---------------------------
@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    list_filter = ('category',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


# ---------------------------
# Category Admin
# ---------------------------
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'main_type')
    list_filter = ('main_type',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


# ---------------------------
# MainType Admin
# ---------------------------
@admin.register(MainType)
class MainTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


# ---------------------------
# Brand Admin
# ---------------------------
@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


# ---------------------------
# Breed Admin
# ---------------------------
@admin.register(Breed)
class BreedAdmin(admin.ModelAdmin):
    list_display = ('name', 'main_type')
    list_filter = ('main_type',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}



@admin.register(TopDeal)
class TopDealAdmin(admin.ModelAdmin):
    list_display = ("title", "main_type", "created_at")  # columns in list view
    list_filter = ("main_type", "created_at")           # filters on the right
    search_fields = ("title", "description")            # search bar
    ordering = ("-created_at",)                         # newest first
    readonly_fields = ("created_at",)                   # can't edit created_at

    fieldsets = (
        (None, {
            "fields": ("main_type", "title", "description", "image", "link")
        }),
        ("Metadata", {
            "fields": ("created_at",),
            "classes": ("collapse",),
        }),
    )

