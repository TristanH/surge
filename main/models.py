from django.db import models
from django.contrib.auth.models import User


class HungryUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # TODO: stripe user info here


class Order(models.Model):
    hungry_user = models.ForeignKey(HungryUser)
    
    IN_BIDDING = 'IB'
    NO_BID = 'NB'
    SUCCESSFUL = "SU"
    YEAR_IN_SCHOOL_CHOICES = (
        (IN_BIDDING, 'In Bidding'),
        (NO_BID, 'No Bid'),
        (SUCCESSFUL, 'Successful'),
    )


class Restuarant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Keyword(models.Model):
    string = models.CharField(max_length=255)


class KeywordGroup(models.Model):
    tags = models.ManyToManyField(Keyword)