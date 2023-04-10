from django.db import models
from django.contrib.auth.models import User

NEIGHBORHOOD_CHOICES = (
    ('Shadyside', 'SHADYSIDE'),
    ('Squirrel Hill North', 'SQUIRREL HILL NORTH'),
    ('Squirrel Hill South', 'SQUIRREL HILL SOUTH'),
    ('Oakland', 'OAKLAND'),
    ('East Libery', 'EAST LIBERTY'),
    ('Downtown', 'DOWNTOWN'),
    ('Southside', 'SOUTHSIDE')
)

GENDER_CHOICES = (
    ('Male', 'MALE'),
    ('Female', 'FEMALE'),
    ('Unspecified', 'UNSPECIFIED'),
)

USER_CHOICES = (
    ('Ski', 'SKI'),
    ('Snowboard', 'SNOWBOARD'),
)


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    neighborhood = models.CharField(max_length=25,
                                    choices=NEIGHBORHOOD_CHOICES,
                                    default='Shadyside')
    height = models.DecimalField(max_digits=10, decimal_places=2)
    gender = models.CharField(max_length=25,
                              choices=GENDER_CHOICES, default='Male')
    bootSize = models.DecimalField(max_digits=10, decimal_places=2)
    userType = models.CharField(max_length=10,
                                choices=USER_CHOICES, default='Ski')

    def __str__(self):
        return f'id={self.id}, user="{self.user}"'
