# home/admin.py
from django.contrib import admin
from .models import SiteSettings, About, HighlightCard, ReasonToLove, VetConsultationReason, Doctor, PetType

admin.site.register(SiteSettings)
admin.site.register(About)
admin.site.register(HighlightCard)
admin.site.register(ReasonToLove)
admin.site.register(VetConsultationReason)
admin.site.register(Doctor)
admin.site.register(PetType)


# @admin.register(Doctor)
# class DoctorAdmin(admin.ModelAdmin):
#     list_display = ("name", "specialization", "experience", "qualification")


# from django.contrib import admin
# from .models import 

# @admin.register(About)
# class AboutAdmin(admin.ModelAdmin):
#     list_display = ('title', 'created_at')
