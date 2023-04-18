from django.contrib.auth.models import User
from django.db import models


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

SKILL_LEVEL = (
    ('Beginner', 'BEGINNER'),
    ('Intermediate', 'INTERMEDIATE'),
    ('Advanced', 'ADVANCED'),
    ('Expert', 'EXPERT'),
)

WEAR_STATUS = (
    ('Factory-New', 'FACTORY-NEW'),
    ('Minimal-Wear', 'MINIMAL-WEAR'),
    ('Field-Tested', 'FIELD-TESTED'),
    ('Well-Worn', 'WELL-WORN'),
    ('Battle-Scarred', 'BATTLE-SCARRED'),
)


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    firstName = models.CharField(max_length=40)
    lastName = models.CharField(max_length=50)
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


class Equipment(models.Model):
    profileId = models.ForeignKey(Profile, on_delete=models.PROTECT)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, max_length=1000)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    equipmentProductName = models.CharField(max_length=1000)
    bindingsProductName = models.CharField(max_length=1000)
    bootsProductName = models.CharField(max_length=1000)
    skillLevel = models.CharField(max_length=25,
                                  choices=SKILL_LEVEL, default='Beginner')
    equipmentHeight = models.DecimalField(max_digits=10, decimal_places=2)
    bootSize = models.DecimalField(max_digits=10, decimal_places=1)
    wearStatus = models.CharField(max_length=25,
                                  choices=WEAR_STATUS, default='Factory-New')
    equipmentType = models.CharField(max_length=10,
                                     choices=USER_CHOICES, default='Ski')

    def __str__(self):
        return f'id={self.id}, profile="{self.profileId}"'


class EquipmentImages(models.Model):
    image = models.FileField(blank=True)
    content_type = models.CharField(max_length=50)
    equipmentId = models.ForeignKey(Equipment, on_delete=models.PROTECT)

    def __str__(self):
        return f'id={self.id}, equipment="{self.equipmentId}"'


class EquipmentListing(models.Model):
    equipmentId = models.ForeignKey(Equipment, 
                                    on_delete=models.PROTECT, 
                                    related_name='equipment_listings')
    profileId = models.ForeignKey(Profile, on_delete=models.PROTECT)
    startDate = models.DateTimeField()
    endDate = models.DateTimeField()

    def __str__(self):
        return f'id={self.id}, equipment="{self.equipmentId}"'


class EquipmentReservation(models.Model):
    equipmentId = models.ForeignKey(Equipment, on_delete=models.PROTECT)
    profileId = models.ForeignKey(Profile, on_delete=models.PROTECT)
    startDate = models.DateTimeField()
    endDate = models.DateTimeField()

    def __str__(self):
        return f'id={self.id}, equipment="{self.equipmentId}"'
