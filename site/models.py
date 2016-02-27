from django.db import models
from django.contrib.auth.models import User


class HungryUser(models.Model)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # TODO: stripe user info here


class Order(models.Model)
    hungry_user = models.ForeignKey(HungryUser)


class Restuarant(models.Model)
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Keyword(models.Model)
    string = models.


class KeywordGroup(models.Model)
    tags = models.ManyToManyField(Keyword)