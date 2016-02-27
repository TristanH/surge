from datetime import datetime, timedelta

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist


class Keyword(models.Model):
    string = models.CharField(max_length=255)
    is_main = models.BooleanField()


class KeywordGroup(models.Model):
    tags = models.ManyToManyField(Keyword)


class HungryUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # TODO: stripe user info here


class Order(models.Model):
    hungry_user = models.ForeignKey(HungryUser)

    was_successful = models.NullBooleanField()

    bidding_end_time = models.DateTimeField(default=datetime.now() + timedelta(seconds=90))

    keywords = models.ForeignKey(KeywordGroup)

    latitude = models.DecimalField(max_digits=10, decimal_places=7)
    longitude = models.DecimalField(max_digits=10, decimal_places=7)

    description = models.CharField(max_length=511, null=True)
    # TODO: stripe payment token


class Restuarant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=10, decimal_places=7)
    longitude = models.DecimalField(max_digits=10, decimal_places=7)


def get_restaurant(self):
    try:
        return Restuarant.objects.get(user=self.id)
    except ObjectDoesNotExist:
        return None

User.add_to_class('restaurant', get_restaurant)


class Item(models.Model):
    name = models.CharField(max_length=255)

    # TODO: do we need min price here

    restaurant = models.ForeignKey(Restuarant)

    keywords = models.ForeignKey(KeywordGroup)

    description = models.CharField(max_length=511)


class Bid(models.Model):
    item = models.ForeignKey(Item)
    order = models.ForeignKey(Order)
    won = models.NullBooleanField()

    @property
    def restaurant(self):
        return self.item.restaurant
