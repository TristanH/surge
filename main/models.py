from django.db import models
from django.contrib.auth.models import User


class Keyword(models.Model):
    string = models.CharField(max_length=255)


class KeywordGroup(models.Model):
    tags = models.ManyToManyField(Keyword)


class HungryUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # TODO: stripe user info here


class Order(models.Model):
    hungry_user = models.ForeignKey(HungryUser)

    IN_BIDDING = 'IB'
    NO_BID = 'NB'
    SUCCESSFUL = "SU"
    STATUSES = (
        (IN_BIDDING, 'In Bidding'),
        (NO_BID, 'No Bid'),
        (SUCCESSFUL, 'Successful'),
    )
    status = models.CharField(max_length=2,
                              choices=STATUSES,
                              default=IN_BIDDING)

    keywords = models.ForeignKey(KeywordGroup)

    latitude = models.DecimalField(max_digits=10, decimal_places=7)
    longitude = models.DecimalField(max_digits=10, decimal_places=7)

    # TODO: stripe payment token


class Restuarant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    latitude = models.DecimalField(max_digits=10, decimal_places=7)
    longitude = models.DecimalField(max_digits=10, decimal_places=7)


class Item(models.Model):
    name = models.CharField(max_length=255)

    # TODO: do we need min price here

    restaurant = models.ForeignKey(Restuarant)

    keywords = models.ForeignKey(KeywordGroup)


class Bid(models.Model):
    item = models.ForeignKey(Item)
    order = models.ForeignKey(Order)
    won = models.NullBooleanField()

    @property
    def restaurant(self):
        return self.item.restaurant
