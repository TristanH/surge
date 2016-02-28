from datetime import timedelta
from django.utils import timezone

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.utils.encoding import python_2_unicode_compatible


class Keyword(models.Model):
    string = models.CharField(max_length=255)
    is_main = models.BooleanField()

    def __str__(self):
        # if self.is_main:
        #     return "Main: " + self.string
        # else:
        #     return self.string
        return self.string


class KeywordGroup(models.Model):
    tags = models.ManyToManyField(Keyword)

    def __str__(self):
        tags = ["#" + str(tag) for tag in (list(self.tags.filter(is_main=True)) + list(self.tags.filter(is_main=False)))]

        if self.tags:
            return ", ".join(tags)
        else:
            return "None"


class HungryUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # TODO: stripe user info here


def bid_time():
    return timezone.now() + timedelta(seconds=90)

class Order(models.Model):
    hungry_user = models.ForeignKey(HungryUser)

    was_successful = models.NullBooleanField()

    bidding_end_time = models.DateTimeField(default=bid_time)

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
    address = models.CharField(max_length=255, default="3180 18th St.")

    def __str__(self):
        return self.name


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

    image_url = models.CharField(max_length=1023, null=True)

    def __str__(self):
        return self.name


class Bid(models.Model):
    item = models.ForeignKey(Item, null=True)
    order = models.ForeignKey(Order)
    won = models.NullBooleanField()

    # In cents
    price = models.IntegerField()

    @property
    def restaurant(self):
        return self.item.restaurant

    @staticmethod
    def make_default(order_id):
        bid = Bid(price=1500, order_id=order_id)
        bid.save()
        return bid
