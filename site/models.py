from django.db import models
from django.contrib.auth.models import User


class HungryUser(models.Model)
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Order(models.Model)
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Restuarant(models.Model)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
