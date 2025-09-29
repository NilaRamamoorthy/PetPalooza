from .models import MainType

def main_types_context(request):
    main_types = MainType.objects.prefetch_related('categories__subcategories')
    return {'main_types': main_types}

from django.urls import resolve
from .models import MainType, Category, SubCategory, Product

def breadcrumbs(request):
    """
    Returns breadcrumb trail based on the current URL.
    Example: Home / Dog / Food / Dry Food / Product
    """
    path = request.path.strip("/").split("/")
    crumbs = [{"name": "Home", "url": "/"}]

    if not path or path[0] == "":
        return {"breadcrumbs": crumbs}

    try:
        if len(path) >= 1:
            main_type = MainType.objects.filter(slug=path[0]).first()
            if main_type:
                crumbs.append({"name": main_type.name, "url": f"/{main_type.slug}/"})

        if len(path) >= 2:
            category = Category.objects.filter(slug=path[1]).first()
            if category:
                crumbs.append({
                    "name": category.name,
                    "url": f"/{category.main_type.slug}/{category.slug}/"
                })

        if len(path) >= 3:
            subcategory = SubCategory.objects.filter(slug=path[2]).first()
            if subcategory:
                crumbs.append({
                    "name": subcategory.name,
                    "url": f"/{subcategory.category.main_type.slug}/{subcategory.category.slug}/{subcategory.slug}/"
                })

        if len(path) >= 4:
            product = Product.objects.filter(slug=path[-1]).first()
            if product:
                crumbs.append({"name": product.name, "url": ""})  # last one no link
    except Exception:
        pass

    return {"breadcrumbs": crumbs}
