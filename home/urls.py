# home/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),           # Home page
    path("about/", views.about_view, name="about"),   # About page
    path('search/', views.search, name='search'),
    path('contact/', views.contact_view, name='contact'),
    path('consult-vet/', views.consult_a_vet_view, name='consult_a_vet'),
    path("consult-doctor/", views.consult_doctor, name="consult_doctor"),
    
]
