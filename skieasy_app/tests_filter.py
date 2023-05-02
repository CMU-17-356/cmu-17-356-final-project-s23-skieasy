from django.test import TestCase, RequestFactory

from skieasy_app.filters import EquipmentFilter
from skieasy_app.models import Equipment, Profile, User


class EquipmentFilterTest(TestCase):

    def setUp(self):
        user = User.objects.create(
            username="ty",
            email="ty@gmail.com",
            first_name="Tyler",
            last_name="Lo",
        )
        tyler = Profile.objects.create(
            user=user,
            first_name='Tyler',
            last_name='Lo',
            neighborhood='Shadyside',
            height=5.6,
            gender='Male',
            boot_size=9.0,
            user_type='Ski'
        )
        self.tyler = tyler
        robyn = Profile.objects.create(
            user=user,
            first_name='Robyn',
            last_name='Last',
            neighborhood='Oakland',
            height=5.2,
            gender='Female',
            boot_size=6.5,
            user_type='Snowboard'
        )
        self.robyn = robyn
        tyler_ski = Equipment.objects.create(
            profile_id=tyler,
            title="Tyler Skis",
            description="Dummy Description",
            price=22,
            equipment_product_name="Dummy Product Name",
            bindings_product_name="Dummy Bindings Name",
            boots_product_name="Dummy Boots Name",
            skill_level="Advanced",
            equipment_height=70,
            boot_size=9.0,
            wear_status="Minimal-Wear",
            equipment_type="Ski",
        )
        self.tyler_ski = tyler_ski
        robyn_board = Equipment.objects.create(
            profile_id=robyn,
            title="Robyn Snowboard",
            description="Dummy Description",
            price=15,
            equipment_product_name="Dummy Product Name",
            bindings_product_name="Dummy Bindings Name",
            boots_product_name="Dummy Boots Name",
            skill_level="Beginner",
            equipment_height=62,
            boot_size=6.5,
            wear_status="Field-Tested",
            equipment_type="Snowboard",
        )
        self.robyn_board = robyn_board
        self.factory = RequestFactory()

    def test_min_price_filter_low(self):
        request = self.factory.get(
            path='/home',
            data={'min_price': 10},
        )
        filtered = EquipmentFilter(
            request.GET,
            queryset=Equipment.objects.all(),
            request=request,
        )
        self.assertEqual(len(filtered.qs), 2)
        self.assertEqual(set(filtered.qs), {self.robyn_board, self.tyler_ski})

    def test_min_price_filter_low_boundary(self):
        request = self.factory.get(
            path='/home',
            data={'min_price': 15},
        )
        filtered = EquipmentFilter(
            request.GET,
            queryset=Equipment.objects.all(),
            request=request,
        )
        self.assertEqual(len(filtered.qs), 2)
        self.assertEqual(set(filtered.qs), {self.robyn_board, self.tyler_ski})

    def test_min_price_filter_mid(self):
        request = self.factory.get(
            path='/home',
            data={'min_price': 20},
        )
        filtered = EquipmentFilter(
            request.GET,
            queryset=Equipment.objects.all(),
            request=request,
        )
        self.assertEqual(len(filtered.qs), 1)
        self.assertEqual(set(filtered.qs), {self.tyler_ski})

    def test_min_price_filter_high_boundary(self):
        request = self.factory.get(
            path='/home',
            data={'min_price': 22},
        )
        filtered = EquipmentFilter(
            request.GET,
            queryset=Equipment.objects.all(),
            request=request,
        )
        self.assertEqual(len(filtered.qs), 1)
        self.assertEqual(set(filtered.qs), {self.tyler_ski})

    def test_min_price_filter_high(self):
        request = self.factory.get(
            path='/home',
            data={'min_price': 25},
        )
        filtered = EquipmentFilter(
            request.GET,
            queryset=Equipment.objects.all(),
            request=request,
        )
        self.assertEqual(len(filtered.qs), 0)
        self.assertEqual(set(filtered.qs), set())

    def test_max_price_filter_low(self):
        request = self.factory.get(
            path='/home',
            data={'max_price': 10},
        )
        filtered = EquipmentFilter(
            request.GET,
            queryset=Equipment.objects.all(),
            request=request,
        )
        self.assertEqual(len(filtered.qs), 0)
        self.assertEqual(set(filtered.qs), set())

    def test_max_price_filter_low_boundary(self):
        request = self.factory.get(
            path='/home',
            data={'max_price': 15},
        )
        filtered = EquipmentFilter(
            request.GET,
            queryset=Equipment.objects.all(),
            request=request,
        )
        self.assertEqual(len(filtered.qs), 1)
        self.assertEqual(set(filtered.qs), {self.robyn_board})

    def test_max_price_filter_low_mid(self):
        request = self.factory.get(
            path='/home',
            data={'max_price': 20},
        )
        filtered = EquipmentFilter(
            request.GET,
            queryset=Equipment.objects.all(),
            request=request,
        )
        self.assertEqual(len(filtered.qs), 1)
        self.assertEqual(set(filtered.qs), {self.robyn_board})

    def test_max_price_filter_low_high_boundary(self):
        request = self.factory.get(
            path='/home',
            data={'max_price': 22},
        )
        filtered = EquipmentFilter(
            request.GET,
            queryset=Equipment.objects.all(),
            request=request,
        )
        self.assertEqual(len(filtered.qs), 2)
        self.assertEqual(set(filtered.qs), {self.robyn_board, self.tyler_ski})

    def test_max_price_filter_low_high(self):
        request = self.factory.get(
            path='/home',
            data={'max_price': 30},
        )
        filtered = EquipmentFilter(
            request.GET,
            queryset=Equipment.objects.all(),
            request=request,
        )
        self.assertEqual(len(filtered.qs), 2)
        self.assertEqual(set(filtered.qs), {self.robyn_board, self.tyler_ski})

    def test_equipment_type_filter_either(self):
        request = self.factory.get(
            path='/home',
            data={},
        )
        filtered = EquipmentFilter(
            request.GET,
            queryset=Equipment.objects.all(),
            request=request,
        )
        self.assertEqual(len(filtered.qs), 2)
        self.assertEqual(set(filtered.qs), {self.robyn_board, self.tyler_ski})

    def test_equipment_type_filter_ski(self):
        request = self.factory.get(
            path='/home',
            data={'equipment_type': 'Ski'},
        )
        filtered = EquipmentFilter(
            request.GET,
            queryset=Equipment.objects.all(),
            request=request,
        )
        self.assertEqual(len(filtered.qs), 1)
        self.assertEqual(set(filtered.qs), {self.tyler_ski})

    def test_equipment_type_filter_snowboard(self):
        request = self.factory.get(
            path='/home',
            data={'equipment_type': 'Snowboard'},
        )
        filtered = EquipmentFilter(
            request.GET,
            queryset=Equipment.objects.all(),
            request=request,
        )
        self.assertEqual(len(filtered.qs), 1)
        self.assertEqual(set(filtered.qs), {self.robyn_board})

    def test_neighborhoods_filter_shadyside(self):
        request = self.factory.get(
            path='/home',
            data={'neighborhoods': 'Shadyside'},
        )
        filtered = EquipmentFilter(
            request.GET,
            queryset=Equipment.objects.all(),
            request=request,
        )
        self.assertEqual(len(filtered.qs), 1)
        self.assertEqual(set(filtered.qs), {self.tyler_ski})

    def test_neighborhoods_filter_oakland(self):
        request = self.factory.get(
            path='/home',
            data={'neighborhoods': 'Oakland'},
        )
        filtered = EquipmentFilter(
            request.GET,
            queryset=Equipment.objects.all(),
            request=request,
        )
        self.assertEqual(len(filtered.qs), 1)
        self.assertEqual(set(filtered.qs), {self.robyn_board})

    def test_neighborhoods_filter_both(self):
        request = self.factory.get(
            path='/home',
            data={'neighborhoods': 'Oakland,Shadyside'},
        )
        filtered = EquipmentFilter(
            request.GET,
            queryset=Equipment.objects.all(),
            request=request,
        )
        self.assertEqual(len(filtered.qs), 2)
        self.assertEqual(set(filtered.qs), {self.tyler_ski, self.robyn_board})

    def test_neighborhoods_filter_both_and_more(self):
        request = self.factory.get(
            path='/home',
            data={'neighborhoods': 'Southside,Oakland,Downtown,Shadyside'},
        )
        filtered = EquipmentFilter(
            request.GET,
            queryset=Equipment.objects.all(),
            request=request,
        )
        self.assertEqual(len(filtered.qs), 2)
        self.assertEqual(set(filtered.qs), {self.tyler_ski, self.robyn_board})

    def test_neighborhoods_filter_none(self):
        request = self.factory.get(
            path='/home',
            data={'neighborhoods': 'Southside,Downtown,Squirrel Hill North'},
        )
        filtered = EquipmentFilter(
            request.GET,
            queryset=Equipment.objects.all(),
            request=request,
        )
        self.assertEqual(len(filtered.qs), 0)
        self.assertEqual(set(filtered.qs), set())

    def test_gender_filter_unspecified(self):
        request = self.factory.get(
            path='/home',
            data={},
        )
        filtered = EquipmentFilter(
            request.GET,
            queryset=Equipment.objects.all(),
            request=request,
        )
        self.assertEqual(len(filtered.qs), 2)
        self.assertEqual(set(filtered.qs), {self.robyn_board, self.tyler_ski})

    def test_gender_filter_male(self):
        request = self.factory.get(
            path='/home',
            data={'gender': 'Male'},
        )
        filtered = EquipmentFilter(
            request.GET,
            queryset=Equipment.objects.all(),
            request=request,
        )
        self.assertEqual(len(filtered.qs), 1)
        self.assertEqual(set(filtered.qs), {self.tyler_ski})

    def test_gender_filter_female(self):
        request = self.factory.get(
            path='/home',
            data={'gender': 'Female'},
        )
        filtered = EquipmentFilter(
            request.GET,
            queryset=Equipment.objects.all(),
            request=request,
        )
        self.assertEqual(len(filtered.qs), 1)
        self.assertEqual(set(filtered.qs), {self.robyn_board})

    def test_boot_size_filter_match_board(self):
        request = self.factory.get(
            path='/home',
            data={'boot_size': 6.5},
        )
        filtered = EquipmentFilter(
            request.GET,
            queryset=Equipment.objects.all(),
            request=request,
        )
        self.assertEqual(len(filtered.qs), 1)
        self.assertEqual(set(filtered.qs), {self.robyn_board})

    def test_boot_size_filter_match_ski(self):
        request = self.factory.get(
            path='/home',
            data={'boot_size': 9.0},
        )
        filtered = EquipmentFilter(
            request.GET,
            queryset=Equipment.objects.all(),
            request=request,
        )
        self.assertEqual(len(filtered.qs), 1)
        self.assertEqual(set(filtered.qs), {self.tyler_ski})

    def test_boot_size_filter_none(self):
        request = self.factory.get(
            path='/home',
            data={'boot_size': 9.5},
        )
        filtered = EquipmentFilter(
            request.GET,
            queryset=Equipment.objects.all(),
            request=request,
        )
        self.assertEqual(len(filtered.qs), 0)
        self.assertEqual(set(filtered.qs), set())

    def test_equipment_height_filter_match(self):
        request = self.factory.get(
            path='/home',
            data={'equipment_height': 70},
        )
        filtered = EquipmentFilter(
            request.GET,
            queryset=Equipment.objects.all(),
            request=request,
        )
        self.assertEqual(len(filtered.qs), 1)
        self.assertEqual(set(filtered.qs), {self.tyler_ski})

    def test_equipment_height_filter_none(self):
        request = self.factory.get(
            path='/home',
            data={'equipment_height': 65},
        )
        filtered = EquipmentFilter(
            request.GET,
            queryset=Equipment.objects.all(),
            request=request,
        )
        self.assertEqual(len(filtered.qs), 0)
        self.assertEqual(set(filtered.qs), set())

    def test_min_boot_size_filter_low(self):
        request = self.factory.get(
            path='/home',
            data={'min_boot_size': 6.0},
        )
        filtered = EquipmentFilter(
            request.GET,
            queryset=Equipment.objects.all(),
            request=request,
        )
        self.assertEqual(len(filtered.qs), 2)
        self.assertEqual(set(filtered.qs), {self.robyn_board, self.tyler_ski})

    def test_min_boot_size_filter_low_boundary(self):
        request = self.factory.get(
            path='/home',
            data={'min_boot_size': 6.5},
        )
        filtered = EquipmentFilter(
            request.GET,
            queryset=Equipment.objects.all(),
            request=request,
        )
        self.assertEqual(len(filtered.qs), 2)
        self.assertEqual(set(filtered.qs), {self.robyn_board, self.tyler_ski})

    def test_min_boot_size_filter_mid(self):
        request = self.factory.get(
            path='/home',
            data={'min_boot_size': 8},
        )
        filtered = EquipmentFilter(
            request.GET,
            queryset=Equipment.objects.all(),
            request=request,
        )
        self.assertEqual(len(filtered.qs), 1)
        self.assertEqual(set(filtered.qs), {self.tyler_ski})

    def test_min_boot_size_filter_high_boundary(self):
        request = self.factory.get(
            path='/home',
            data={'min_boot_size': 9},
        )
        filtered = EquipmentFilter(
            request.GET,
            queryset=Equipment.objects.all(),
            request=request,
        )
        self.assertEqual(len(filtered.qs), 1)
        self.assertEqual(set(filtered.qs), {self.tyler_ski})

    def test_min_boot_size_filter_high(self):
        request = self.factory.get(
            path='/home',
            data={'min_boot_size': 10.5},
        )
        filtered = EquipmentFilter(
            request.GET,
            queryset=Equipment.objects.all(),
            request=request,
        )
        self.assertEqual(len(filtered.qs), 0)
        self.assertEqual(set(filtered.qs), set())

    def test_max_boot_size_filter_low(self):
        request = self.factory.get(
            path='/home',
            data={'max_boot_size': 6.0},
        )
        filtered = EquipmentFilter(
            request.GET,
            queryset=Equipment.objects.all(),
            request=request,
        )
        self.assertEqual(len(filtered.qs), 0)
        self.assertEqual(set(filtered.qs), set())

    def test_max_boot_size_filter_low_boundary(self):
        request = self.factory.get(
            path='/home',
            data={'max_boot_size': 6.5},
        )
        filtered = EquipmentFilter(
            request.GET,
            queryset=Equipment.objects.all(),
            request=request,
        )
        self.assertEqual(len(filtered.qs), 1)
        self.assertEqual(set(filtered.qs), {self.robyn_board})

    def test_max_boot_size_filter_mid(self):
        request = self.factory.get(
            path='/home',
            data={'max_boot_size': 8},
        )
        filtered = EquipmentFilter(
            request.GET,
            queryset=Equipment.objects.all(),
            request=request,
        )
        self.assertEqual(len(filtered.qs), 1)
        self.assertEqual(set(filtered.qs), {self.robyn_board})

    def test_max_boot_size_filter_high_boundary(self):
        request = self.factory.get(
            path='/home',
            data={'max_boot_size': 9.0},
        )
        filtered = EquipmentFilter(
            request.GET,
            queryset=Equipment.objects.all(),
            request=request,
        )
        self.assertEqual(len(filtered.qs), 2)
        self.assertEqual(set(filtered.qs), {self.robyn_board, self.tyler_ski})

    def test_max_boot_size_filter_high(self):
        request = self.factory.get(
            path='/home',
            data={'max_boot_size': 10.5},
        )
        filtered = EquipmentFilter(
            request.GET,
            queryset=Equipment.objects.all(),
            request=request,
        )
        self.assertEqual(len(filtered.qs), 2)
        self.assertEqual(set(filtered.qs), {self.robyn_board, self.tyler_ski})

    def test_min_equipment_height_filter_low(self):
        request = self.factory.get(
            path='/home',
            data={'min_equipment_height': 60.5},
        )
        filtered = EquipmentFilter(
            request.GET,
            queryset=Equipment.objects.all(),
            request=request,
        )
        self.assertEqual(len(filtered.qs), 2)
        self.assertEqual(set(filtered.qs), {self.robyn_board, self.tyler_ski})

    def test_min_equipment_height_filter_low_boundary(self):
        request = self.factory.get(
            path='/home',
            data={'min_equipment_height': 62},
        )
        filtered = EquipmentFilter(
            request.GET,
            queryset=Equipment.objects.all(),
            request=request,
        )
        self.assertEqual(len(filtered.qs), 2)
        self.assertEqual(set(filtered.qs), {self.robyn_board, self.tyler_ski})

    def test_min_equipment_height_filter_mid(self):
        request = self.factory.get(
            path='/home',
            data={'min_equipment_height': 65},
        )
        filtered = EquipmentFilter(
            request.GET,
            queryset=Equipment.objects.all(),
            request=request,
        )
        self.assertEqual(len(filtered.qs), 1)
        self.assertEqual(set(filtered.qs), {self.tyler_ski})

    def test_min_equipment_height_filter_high_boundary(self):
        request = self.factory.get(
            path='/home',
            data={'min_equipment_height': 70},
        )
        filtered = EquipmentFilter(
            request.GET,
            queryset=Equipment.objects.all(),
            request=request,
        )
        self.assertEqual(len(filtered.qs), 1)
        self.assertEqual(set(filtered.qs), {self.tyler_ski})

    def test_min_equipment_height_filter_high(self):
        request = self.factory.get(
            path='/home',
            data={'min_equipment_height': 71},
        )
        filtered = EquipmentFilter(
            request.GET,
            queryset=Equipment.objects.all(),
            request=request,
        )
        self.assertEqual(len(filtered.qs), 0)
        self.assertEqual(set(filtered.qs), set())

    def test_max_equipment_height_filter_low(self):
        request = self.factory.get(
            path='/home',
            data={'max_equipment_height': 61},
        )
        filtered = EquipmentFilter(
            request.GET,
            queryset=Equipment.objects.all(),
            request=request,
        )
        self.assertEqual(len(filtered.qs), 0)
        self.assertEqual(set(filtered.qs), set())

    def test_max_equipment_height_filter_low_boundary(self):
        request = self.factory.get(
            path='/home',
            data={'max_equipment_height': 62},
        )
        filtered = EquipmentFilter(
            request.GET,
            queryset=Equipment.objects.all(),
            request=request,
        )
        self.assertEqual(len(filtered.qs), 1)
        self.assertEqual(set(filtered.qs), {self.robyn_board})

    def test_max_equipment_height_filter_mid(self):
        request = self.factory.get(
            path='/home',
            data={'max_equipment_height': 69},
        )
        filtered = EquipmentFilter(
            request.GET,
            queryset=Equipment.objects.all(),
            request=request,
        )
        self.assertEqual(len(filtered.qs), 1)
        self.assertEqual(set(filtered.qs), {self.robyn_board})

    def test_max_equipment_height_filter_high_boundary(self):
        request = self.factory.get(
            path='/home',
            data={'max_equipment_height': 70},
        )
        filtered = EquipmentFilter(
            request.GET,
            queryset=Equipment.objects.all(),
            request=request,
        )
        self.assertEqual(len(filtered.qs), 2)
        self.assertEqual(set(filtered.qs), {self.tyler_ski, self.robyn_board})

    def test_max_equipment_height_filter_high(self):
        request = self.factory.get(
            path='/home',
            data={'max_equipment_height': 71},
        )
        filtered = EquipmentFilter(
            request.GET,
            queryset=Equipment.objects.all(),
            request=request,
        )
        self.assertEqual(len(filtered.qs), 2)
        self.assertEqual(set(filtered.qs), {self.tyler_ski, self.robyn_board})
