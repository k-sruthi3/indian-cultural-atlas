# culture/admin.py
from django.contrib import admin
from .models import State, Festival, DanceForm, District
@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ['name', 'capital']  # ONLY existing fields
    search_fields = ['name', 'capital']

@admin.register(Festival)
class FestivalAdmin(admin.ModelAdmin):
    list_display = ['name', 'state']
    list_filter = ['state']

@admin.register(DanceForm)
class DanceFormAdmin(admin.ModelAdmin):
    list_display = ['name', 'state', 'classical']
@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ['name', 'state']
    list_filter = ['state']
    search_fields = ['name']
