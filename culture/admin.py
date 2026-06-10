# admin.py
from django.contrib import admin
from .models import State, Festival, DanceForm, District, Submission


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ['name', 'capital']
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


# ----------------------------
# Submission Actions
# ----------------------------

@admin.action(description="Approve selected submissions")
def approve_submissions(modeladmin, request, queryset):

    for sub in queryset:

        # Skip already approved submissions
        if sub.status == "approved":
            continue

        # --------------------
        # STATE SUBMISSION
        # --------------------
        if sub.area_type == "state":

            State.objects.get_or_create(
                name=sub.state_name,
                defaults={
                    "capital": sub.capital,

                    "famous_food": sub.famous_food,
                    "food_image": sub.food_image,
                    "food_link": sub.food_link,

                    "famous_dance": sub.famous_dance,
                    "dance_image": sub.dance_image,
                    "dance_link": sub.dance_link,

                    "famous_folk_art": sub.famous_folk_art,
                    "folk_art_image": sub.folk_art_image,
                    "folk_art_link": sub.folk_art_link,

                    "famous_temple": sub.famous_temple,
                    "temple_image": sub.temple_image,
                    "temple_link": sub.temple_link,

                    "traditional_dress": sub.traditional_dress,
                    "dress_image": sub.dress_image,
                    "dress_link": sub.dress_link,

                    "monuments": sub.monuments,
                    "monument_image": sub.monument_image,
                    "monument_link": sub.monument_link,

                    "uniqueness": sub.uniqueness,
                    "image": sub.image,
                }
            )

        # --------------------
        # DISTRICT SUBMISSION
        # --------------------
        elif sub.area_type == "district":

            state, created = State.objects.get_or_create(
                name=sub.state_name,
                defaults={
                    "capital": sub.capital or "Unknown"
                }
            )

            District.objects.get_or_create(
    name=sub.district_name,
    state=state,
    defaults={
        "famous_food": sub.famous_food,
        "food_link": sub.food_link,

        "famous_festival": sub.famous_festival,
        "festival_link": sub.festival_link,

        "famous_temple": sub.famous_temple,
        "temple_link": sub.temple_link,

        "famous_monument": sub.monuments,
        "monument_link": sub.monument_link,

        "uniqueness": sub.uniqueness,
        "uniqueness_link": sub.uniqueness_link,

        "image": sub.image,
    }
)

        sub.status = "approved"
        sub.save()

@admin.action(description="Reject selected submissions")
def reject_submissions(modeladmin, request, queryset):
    queryset.update(status='rejected')


# ----------------------------
# Submission Admin
# ----------------------------

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = (
        'state_name',
        'district_name',
        'area_type',
        'status',
        'created_at'
    )

    list_filter = (
        'status',
        'area_type'
    )

    search_fields = (
        'state_name',
        'district_name'
    )

    actions = [
        approve_submissions,
        reject_submissions
    ]
    search_fields = (
        'title',
        'state_name',
        'district_name'
    )

    actions = [
        approve_submissions,
        reject_submissions
    ]