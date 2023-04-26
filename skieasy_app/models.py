from django.contrib.auth.models import User
from django.db import models


NEIGHBORHOOD_CHOICES = (
    ('Shadyside', 'SHADYSIDE'),
    ('Squirrel Hill North', 'SQUIRREL HILL NORTH'),
    ('Squirrel Hill South', 'SQUIRREL HILL SOUTH'),
    ('Oakland', 'OAKLAND'),
    ('East Liberty', 'EAST LIBERTY'),
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
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=50)
    neighborhood = models.CharField(
        max_length=25,
        choices=NEIGHBORHOOD_CHOICES,
        default='Shadyside'
    )
    height = models.DecimalField(max_digits=10, decimal_places=2)
    gender = models.CharField(
        max_length=25,
        choices=GENDER_CHOICES,
        default='Male'
    )
    boot_size = models.DecimalField(max_digits=10, decimal_places=2)
    user_type = models.CharField(
        max_length=10,
        choices=USER_CHOICES,
        default='Ski'
    )

    def __str__(self):
        return f'id={self.id}, user="{self.user}"'


class Equipment(models.Model):
    profile_id = models.ForeignKey(Profile, on_delete=models.PROTECT)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, max_length=1000)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    equipment_product_name = models.CharField(max_length=1000)
    bindings_product_name = models.CharField(max_length=1000)
    boots_product_name = models.CharField(max_length=1000)
    skill_level = models.CharField(
        max_length=25,
        choices=SKILL_LEVEL,
        default='Beginner'
    )
    equipment_height = models.DecimalField(max_digits=10, decimal_places=2)
    boot_size = models.DecimalField(max_digits=10, decimal_places=1)
    wear_status = models.CharField(
        max_length=25,
        choices=WEAR_STATUS,
        default='Factory-New'
    )
    equipment_type = models.CharField(
        max_length=10,
        choices=USER_CHOICES,
        default='Ski'
    )

    def __str__(self):
        return f'id={self.id}, profile="{self.profile_id}"'


class EquipmentImage(models.Model):
    image = models.FileField(blank=True)
    content_type = models.CharField(max_length=50)
    equipment_id = models.ForeignKey(Equipment, on_delete=models.PROTECT)

    def __str__(self):
        return f'id={self.id}, equipment="{self.equipment_id}"'


class EquipmentListing(models.Model):
    equipment_id = models.ForeignKey(
        Equipment,
        on_delete=models.PROTECT,
        related_name='equipment_listings'
    )
    profile_id = models.ForeignKey(Profile, on_delete=models.PROTECT)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self):
        return f'id={self.id}, equipment="{self.equipment_id}"'


class EquipmentReservation(models.Model):
    equipment_id = models.ForeignKey(Equipment, on_delete=models.PROTECT)
    profile_id = models.ForeignKey(Profile, on_delete=models.PROTECT)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self):
        return f'id={self.id}, equipment="{self.equipment_id}"'
