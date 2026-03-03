# culture/models.py

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# ----------------------------
# STATE MODEL
# ----------------------------

class State(models.Model):
    name = models.CharField(max_length=100)
    capital = models.CharField(max_length=100)

    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    famous_food = models.TextField(blank=True)
    food_image = models.URLField(blank=True)

    famous_dance = models.TextField(blank=True)
    dance_image = models.URLField(blank=True)

    famous_folk_art = models.TextField(blank=True)
    folk_art_image = models.URLField(blank=True)

    famous_temple = models.TextField(blank=True)
    temple_image = models.URLField(blank=True)

    traditional_dress = models.TextField(blank=True)
    dress_image = models.URLField(blank=True)

    monuments = models.TextField(blank=True)
    monument_image = models.URLField(blank=True)

    uniqueness = models.TextField(blank=True)

    image = models.URLField(blank=True)

    def __str__(self):
        return self.name

    @property
    def google_maps_link(self):
        if self.latitude and self.longitude:
            return f"https://www.google.com/maps?q={self.latitude},{self.longitude}"
        return f"https://www.google.com/maps/search/{self.capital}+India"

    @property
    def google_maps_embed(self):
        if self.latitude and self.longitude:
            return f"https://maps.google.com/maps?q={self.latitude},{self.longitude}&output=embed"
        return f"https://maps.google.com/maps?q={self.capital}+India&output=embed"


# ----------------------------
# FESTIVAL MODEL
# ----------------------------

class Festival(models.Model):
    name = models.CharField(max_length=100)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    description = models.TextField()
    date = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# ----------------------------
# DANCE FORM MODEL
# ----------------------------

class DanceForm(models.Model):
    name = models.CharField(max_length=100)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    description = models.TextField()
    classical = models.BooleanField(default=False)

    def __str__(self):
        return self.name


# ----------------------------
# DISTRICT MODEL
# ----------------------------

class District(models.Model):
    name = models.CharField(max_length=100)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    famous_food = models.TextField(blank=True)
    famous_festival = models.TextField(blank=True)
    famous_temple = models.TextField(blank=True)
    famous_monument = models.TextField(blank=True)
    uniqueness = models.TextField(blank=True)
    image = models.URLField(blank=True)

    def __str__(self):
        return f"{self.name}, {self.state.name}"

    @property
    def google_maps_link(self):
        return f"https://www.google.com/maps/search/{self.name},+{self.state.name}"


# ----------------------------
# PROFILE MODEL
# ----------------------------

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(
        upload_to='profile_pics/',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.user.username

# ----------------------------
# SIGNALS (Auto Create Profile)
# ----------------------------


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)