# home/views.py

from django.shortcuts import render
from .models import About,HighlightCard, ReasonToLove, VetConsultationReason, PetType



# def home(request):
#     pets = PetType.objects.all()
#     return render(request, 'home/home.html', {'pets': pets})

from shop.models import Product, MainType

def home(request):
    pets = PetType.objects.all()  

    dog_healthcare_products = Product.objects.filter(
        main_type__slug="dog",
        category__slug="health-care",
        is_available=True
    )[:10]
    context = {
        "pets": pets,
        "dog_healthcare_products": dog_healthcare_products,
    }
    return render(request, "home/home.html", context)


def about_view(request):
    about = About.objects.last()  # or .first() depending on your data
    cards = HighlightCard.objects.all()
    reason = ReasonToLove.objects.first()  # adjust as needed if multiple

    context = {
        'about': about,
        'cards': cards,
        'reason': reason,
    }

    return render(request, 'home/about.html', context)


def contact_view(request):
    return render(request, 'home/contact.html')



def consult_a_vet_view(request):
    reasons = VetConsultationReason.objects.all().order_by('order')
    doctors = Doctor.objects.all()
    return render(request, 'home/consult_a_vet.html', {'reasons': reasons,'doctors':doctors })



from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Review
from .forms import ReviewForm

def consult_doctor(request):
    """
    Renders the Consult Doctor page with service details and customer reviews.
    """
    # Existing service context
    service_context = {
        "service_name": "Instant Consultation",
        "service_time": "10 AM to 7 PM",
        "price": 299,
        "old_price": 499,
        "discount": "40% OFF",
        "rating": 5,
    }

    # Reviews logic
    reviews = Review.objects.all()
    form = ReviewForm()

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                return JsonResponse({"success": True})
            return redirect("consult_doctor")

    context = {**service_context, "reviews": reviews, "form": form}
    return render(request, "home/consult_doctor.html", context)


from .models import Doctor

def doctors_list(request):
    doctors = Doctor.objects.all()
    return render(request, "doctors.html", {"doctors": doctors})



def search(request):
    query = request.GET.get('q', '')
    # Placeholder: In real use, you'd filter products based on `query`
    return render(request, 'home/search_results.html', {'query': query})



# from django.shortcuts import render
# from shop.models import Product, SubCategory

# def calming_products(request):
#     # Get products under "Dog → Health Care"
#     dog_health_products = Product.objects.filter(
#         main_type__slug="dog",
#         subtype__slug="health-care"
#     )[:6]  # limit to 5 for carousel

#     return render(request, "home/home.html", {
#         "dog_health_products": dog_health_products,
#     })
