from django.urls import path
from . import views

app_name = "cart"

urlpatterns = [
    path("", views.cart_detail, name="cart_detail"),
    path("add/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("remove/<int:item_id>/", views.remove_from_cart, name="remove_from_cart"),
    path("update/<int:item_id>/<str:action>/", views.update_cart, name="update_cart"),
    path("summary/", views.cart_summary, name="cart_summary"),
    path("checkout/", views.checkout, name="checkout"),
    path("order-complete/<int:order_id>/", views.order_complete, name="order_complete"),

]
