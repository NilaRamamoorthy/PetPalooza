from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from shop.models import Product
from .models import Cart, CartItem

@login_required
def get_user_cart(user):
    cart, created = Cart.objects.get_or_create(user=user)
    return cart

from django.shortcuts import redirect, get_object_or_404
from .models import Cart, CartItem
from shop.models import Product

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if not request.user.is_authenticated:
        # If not logged in, redirect to login with next parameter
        return redirect('login')  

    # ✅ FIXED: use request.user (not request.user.user)
    cart, created = Cart.objects.get_or_create(user=request.user)  

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart, 
        product=product
    )
    if not created:
        cart_item.quantity += 1
    cart_item.save()

    return redirect('cart:cart_detail')


@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item.delete()
    return redirect("cart:cart_detail")   # 👈 fixed


def update_cart(request, item_id, action):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)

    if action == "increase":
        item.quantity += 1
        item.save()
    elif action == "decrease":
        if item.quantity > 1:
            item.quantity -= 1
            item.save()
        else:
            item.delete()  # if qty becomes 0, remove item completely

    return redirect("cart:cart_detail")
 # 👈 fixed

# @login_required
# cart/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# cart/views.py
def cart_detail(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        items = CartItem.objects.filter(cart=cart)

        subtotal = sum(item.product.price * item.quantity for item in items)
        shipping = 99 if items else 0
        total = subtotal + shipping

        context = {
            "cart_items": items,
            "subtotal": subtotal,
            "shipping": shipping,
            "total": total,
            "show_login_message": False,
        }
    else:
        # anonymous users → empty cart
        context = {
            "cart_items": [],
            "subtotal": 0,
            "shipping": 0,
            "total": 0,
            "show_login_message": True,
        }

    return render(request, "cart/cart.html", context)


from django.http import JsonResponse

def cart_summary(request):
    if not request.user.is_authenticated:
        return JsonResponse({"subtotal": 0, "shipping": 0, "total": 0})

    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)

    subtotal = sum(item.product.price * item.quantity for item in cart_items)
    shipping = 99 if cart_items else 0
    total = subtotal + shipping

    return JsonResponse({
        "subtotal": subtotal,
        "shipping": shipping,
        "total": total,
    })

from django.shortcuts import render, redirect
from .models import CartItem
from .models import Order  # 👈 import

def checkout(request):
    if not request.user.is_authenticated:
        return redirect("login")

    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)

    subtotal = sum(item.subtotal() for item in cart_items)
    shipping = 99 if subtotal > 0 else 0
    total = subtotal + shipping

    if request.method == "POST":
        # Save order
        order = Order.objects.create(
            first_name=request.POST.get("first_name"),
            last_name=request.POST.get("last_name"),
            email=request.POST.get("email"),
            phone=request.POST.get("phone"),
            address=request.POST.get("address"),
            city=request.POST.get("city"),
            state=request.POST.get("state"),
            pincode=request.POST.get("pincode"),
        )

        # ✅ Clear the cart after successful checkout
        cart_items.delete()

        return redirect("cart:order_complete", order_id=order.id)

    return render(request, "cart/payment.html", {
        "cart_items": cart_items,
        "subtotal": subtotal,
        "shipping": shipping,
        "total": total,
    })


def order_complete(request, order_id):
    order = Order.objects.get(id=order_id)
    return render(request, "cart/order_complete.html", {"order": order})

