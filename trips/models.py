from django.db import models
from django.contrib.auth.models import User
from country_list import countries_for_language

COUNTRIES = [name for code, name in countries_for_language('en')]


# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    home_country = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username
    

class Trip(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trips')
    country = models.CharField(max_length=100)
    date_visited = models.DateField()

    def __str__(self):
        return f'{self.country} visited on {self.date_visited}'