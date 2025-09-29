# home/models.py
from django.db import models

class SiteSettings(models.Model):
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    logo = models.ImageField(upload_to='logos/')

    def __str__(self):
        return "Site Settings"

# About Page

class About(models.Model):
    title = models.CharField(max_length=200)
    mission = models.TextField()
    description = models.TextField()
    image = models.ImageField(upload_to="about_images/")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title



class HighlightCard(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='highlights/')
    link = models.URLField()

class ReasonToLove(models.Model):
    description = models.TextField()
    image = models.ImageField(upload_to='reasons/')


# Consult A Vet

class VetConsultationReason(models.Model):
    title = models.CharField(max_length=100)
    icon = models.ImageField(upload_to='vet_icons/')  # These are the circular icons with pets
    order = models.PositiveIntegerField(default=0)     # Optional: to control display order

    def __str__(self):
        return self.title
    

from django.db import models

class Doctor(models.Model):
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=200)
    experience = models.CharField(max_length=50)
    qualification = models.CharField(max_length=200)
    image = models.ImageField(upload_to="doctors/")  # store doctor image

    def __str__(self):
        return self.name

# Reviews



class Review(models.Model):
    name = models.CharField(max_length=100)
    rating = models.PositiveIntegerField(default=5)  # 1–5 stars
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.rating}★)"


# Home
from django.db import models

class PetType(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="pets/")  # store pet icons

    def __str__(self):
        return self.name
