import datetime
from django.forms import ValidationError
from django.test import TestCase
from django.utils import timezone
from decimal import Decimal

from skieasy_app.models import Equipment, EquipmentListing, EquipmentReservation, Profile, User


class ProfileTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(
            username="ty",
            email="ty@gmail.com",
            first_name="Tyler",
            last_name="Lo",
        )

    def test_valid_profile(self):
        tyler = Profile(
            user=self.user,
            first_name='Tyler',
            last_name='Lo',
            neighborhood='Shadyside',
            height=Decimal('5.6'),
            gender='Male',
            boot_size=9.0,
            user_type='Ski'
        )
        tyler.full_clean()
        tyler.save()
        self.assertEqual(tyler.user.username, 'ty')
        self.assertEqual(tyler.first_name, 'Tyler')
        self.assertEqual(tyler.last_name, 'Lo')
        self.assertEqual(tyler.neighborhood, 'Shadyside')
        self.assertEqual(tyler.height, Decimal('5.6'))
        self.assertEqual(tyler.gender, 'Male')
        self.assertEqual(tyler.boot_size, 9.0)
        self.assertEqual(tyler.user_type, 'Ski')
        self.assertEqual(tyler.phone_number, '')

    def test_valid_profile_with_phone(self):
        tyler = Profile(
            user=self.user,
            first_name='Tyler',
            last_name='Lo',
            neighborhood='Shadyside',
            height=Decimal('5.6'),
            gender='Male',
            boot_size=9.0,
            user_type='Ski',
            phone_number='+1 (922) 282 1923'
        )
        tyler.full_clean()
        tyler.save()
        self.assertEqual(tyler.user.username, 'ty')
        self.assertEqual(tyler.first_name, 'Tyler')
        self.assertEqual(tyler.last_name, 'Lo')
        self.assertEqual(tyler.neighborhood, 'Shadyside')
        self.assertEqual(tyler.height, Decimal('5.6'))
        self.assertEqual(tyler.gender, 'Male')
        self.assertEqual(tyler.boot_size, 9.0)
        self.assertEqual(tyler.user_type, 'Ski')
        self.assertEqual(tyler.phone_number, '+1 (922) 282 1923')

    def test_valid_profile_defaults(self):
        tyler = Profile(
            user=self.user,
            first_name='Tyler',
            last_name='Lo',
            neighborhood='Shadyside',
            height=Decimal('5.6'),
            gender='Male',
            boot_size=9.0,
            user_type='Ski',
            phone_number='+1 (922) 282 1923'
        )
        tyler.full_clean()
        tyler.save()
        self.assertEqual(tyler.neighborhood, 'Shadyside')
        self.assertEqual(tyler.gender, 'Male')
        self.assertEqual(tyler.user_type, 'Ski')

    def test_gender_invalid(self):
        try:
            Profile(
                user=self.user,
                first_name='Tyler',
                last_name='Lo',
                neighborhood='Shadyside',
                height=5.6,
                boot_size=9.0,
                user_type='Ski',
                gender='Alien',
            ).full_clean()
            self.fail("should not reach here")
        except ValidationError as error:
            self.assertTrue(
                "not a valid choice" in error.message_dict['gender'][0]
            )

    def test_neighborhood_invalid(self):
        try:
            Profile(
                user=self.user,
                first_name='Tyler',
                last_name='Lo',
                gender='Male',
                height=5.6,
                boot_size=9.0,
                user_type='Ski',
                neighborhood='Shoreline',
            ).full_clean()
            self.fail("should not reach here")
        except ValidationError as error:
            self.assertTrue(
                "not a valid choice" in error.message_dict['neighborhood'][0]
            )

    def test_first_name_long(self):
        try:
            Profile(
                user=self.user,
                last_name='Lo',
                neighborhood='Shadyside',
                height=5.6,
                gender='Male',
                boot_size=9.0,
                user_type='Ski',
                first_name='Tyler' * 9,
            ).full_clean()
            self.fail("should not reach here")
        except ValidationError as error:
            self.assertTrue(
                "at most 40 characters" in error.message_dict['first_name'][0]
            )

    def test_last_name_long(self):
        try:
            Profile(
                user=self.user,
                first_name='Tyler',
                neighborhood='Shadyside',
                height=5.6,
                gender='Male',
                boot_size=9.0,
                user_type='Ski',
                last_name='Lo' * 30,
            ).full_clean()
            self.fail("should not reach here")
        except ValidationError as error:
            self.assertTrue(
                "at most 50 characters" in error.message_dict['last_name'][0]
            )


class EquipmentTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(
            username="ty",
            email="ty@gmail.com",
            first_name="Tyler",
            last_name="Lo",
        )
        self.tyler = Profile.objects.create(
            user=self.user,
            first_name='Tyler',
            last_name='Lo',
            neighborhood='Shadyside',
            height=Decimal('5.6'),
            gender='Male',
            boot_size=9.0,
            user_type='Ski',
            phone_number='+1 (922) 282 1923'
        )

    def test_valid_equipment(self):
        board = Equipment(
            profile_id=self.tyler,
            title="Burton Legion Snowboard",
            description="Nice Board",
            price=Decimal('22'),
            equipment_product_name="Burton Legion Snowboard",
            bindings_product_name="Burton Legion Bindings",
            boots_product_name="Burton Gravity Boots",
            skill_level='Advanced',
            equipment_height=Decimal('70'),
            boot_size=Decimal('9.0'),
            wear_status='Minimal-Wear',
            equipment_type='Snowboard',
        )
        board.full_clean()
        board.save()
        self.assertEqual(board.profile_id.first_name, 'Tyler')
        self.assertEqual(board.title, 'Burton Legion Snowboard')
        self.assertEqual(board.description, 'Nice Board')
        self.assertEqual(board.price, Decimal('22'))
        self.assertEqual(board.equipment_product_name,
                         'Burton Legion Snowboard')
        self.assertEqual(board.bindings_product_name, 'Burton Legion Bindings')
        self.assertEqual(board.boots_product_name, 'Burton Gravity Boots')
        self.assertEqual(board.skill_level, 'Advanced')
        self.assertEqual(board.equipment_height, Decimal('70'))
        self.assertEqual(board.boot_size, Decimal('9.0'))
        self.assertEqual(board.wear_status, 'Minimal-Wear')
        self.assertEqual(board.equipment_type, 'Snowboard')

    def test_valid_equipment_defaults(self):
        board = Equipment(
            profile_id=self.tyler,
            title="Burton Legion Snowboard",
            price=Decimal('22'),
            equipment_product_name="Burton Legion Snowboard",
            bindings_product_name="Burton Legion Bindings",
            boots_product_name="Burton Gravity Boots",
            equipment_height=Decimal('70'),
            boot_size=Decimal('9.0'),
        )
        board.full_clean()
        board.save()
        self.assertEqual(board.description, '')
        self.assertEqual(board.skill_level, 'Beginner')
        self.assertEqual(board.wear_status, 'Factory-New')
        self.assertEqual(board.equipment_type, 'Ski')

    def test_title_long(self):
        try:
            Equipment(
                profile_id=self.tyler,
                title="Burton Legion Snowboard" * 10,
                price=Decimal('22'),
                equipment_product_name="Burton Legion Snowboard",
                bindings_product_name="Burton Legion Bindings",
                boots_product_name="Burton Gravity Boots",
                equipment_height=Decimal('70'),
                boot_size=Decimal('9.0'),
            ).full_clean()
            self.fail("should not reach here")
        except ValidationError as error:
            self.assertTrue(
                "at most 100 characters" in error.message_dict['title'][0]
            )

    def test_price_invalid(self):
        try:
            Equipment(
                profile_id=self.tyler,
                title="Burton Legion Snowboard",
                price=Decimal('22.123'),
                equipment_product_name="Burton Legion Snowboard",
                bindings_product_name="Burton Legion Bindings",
                boots_product_name="Burton Gravity Boots",
                equipment_height=Decimal('70'),
                boot_size=Decimal('9.0'),
            ).full_clean()
            self.fail("should not reach here")
        except ValidationError as error:
            self.assertTrue(
                "no more than 2" in error.message_dict['price'][0]
            )

    def test_equipment_product_long(self):
        try:
            Equipment(
                profile_id=self.tyler,
                title="Burton Legion Snowboard",
                price=Decimal('22'),
                equipment_product_name="Burton Legion Snowboard" * 100,
                bindings_product_name="Burton Legion Bindings",
                boots_product_name="Burton Gravity Boots",
                equipment_height=Decimal('70'),
                boot_size=Decimal('9.0'),
            ).full_clean()
            self.fail("should not reach here")
        except ValidationError as error:
            self.assertTrue(
                "at most 1000 characters"
                in
                error.message_dict['equipment_product_name'][0]
            )

    def test_bindings_product_long(self):
        try:
            Equipment(
                profile_id=self.tyler,
                title="Burton Legion Snowboard",
                price=Decimal('22'),
                equipment_product_name="Burton Legion Snowboard",
                bindings_product_name="Burton Legion Bindings" * 100,
                boots_product_name="Burton Gravity Boots",
                equipment_height=Decimal('70'),
                boot_size=Decimal('9.0'),
            ).full_clean()
            self.fail("should not reach here")
        except ValidationError as error:
            self.assertTrue(
                "at most 1000 characters"
                in
                error.message_dict['bindings_product_name'][0]
            )

    def test_boots_product_long(self):
        try:
            Equipment(
                profile_id=self.tyler,
                title="Burton Legion Snowboard",
                price=Decimal('22'),
                equipment_product_name="Burton Legion Snowboard",
                bindings_product_name="Burton Legion Bindings",
                boots_product_name="Burton Gravity Boots" * 100,
                equipment_height=Decimal('70'),
                boot_size=Decimal('9.0'),
            ).full_clean()
            self.fail("should not reach here")
        except ValidationError as error:
            self.assertTrue(
                "at most 1000 characters"
                in
                error.message_dict['boots_product_name'][0]
            )

    def test_skill_level_invalid(self):
        try:
            Equipment(
                profile_id=self.tyler,
                title="Burton Legion Snowboard",
                price=Decimal('22'),
                equipment_product_name="Burton Legion Snowboard",
                bindings_product_name="Burton Legion Bindings",
                boots_product_name="Burton Gravity Boots",
                equipment_height=Decimal('70'),
                boot_size=Decimal('9.0'),
                skill_level="Rad"
            ).full_clean()
            self.fail("should not reach here")
        except ValidationError as error:
            self.assertTrue(
                "not a valid choice" in error.message_dict['skill_level'][0]
            )

    def test_equipment_height_invalid(self):
        try:
            Equipment(
                profile_id=self.tyler,
                title="Burton Legion Snowboard",
                price=Decimal('22'),
                equipment_product_name="Burton Legion Snowboard",
                bindings_product_name="Burton Legion Bindings",
                boots_product_name="Burton Gravity Boots",
                equipment_height=Decimal('170.222'),
                boot_size=Decimal('9.0'),
            ).full_clean()
            self.fail("should not reach here")
        except ValidationError as error:
            self.assertTrue(
                "no more than 2" 
                in
                error.message_dict['equipment_height'][0]
            )
        try:
            Equipment(
                profile_id=self.tyler,
                title="Burton Legion Snowboard",
                price=Decimal('22'),
                equipment_product_name="Burton Legion Snowboard",
                bindings_product_name="Burton Legion Bindings",
                boots_product_name="Burton Gravity Boots",
                equipment_height='bad value',
                boot_size=Decimal('9.0'),
            ).full_clean()
            self.fail("should not reach here")
        except ValidationError as error:
            self.assertTrue(
                "must be a decimal"
                in
                error.message_dict['equipment_height'][0]
            )

    def test_boot_size_invalid(self):
        try:
            Equipment(
                profile_id=self.tyler,
                title="Burton Legion Snowboard",
                price=Decimal('22'),
                equipment_product_name="Burton Legion Snowboard",
                bindings_product_name="Burton Legion Bindings",
                boots_product_name="Burton Gravity Boots",
                equipment_height=Decimal('70'),
                boot_size=Decimal('9.52'),
            ).full_clean()
            self.fail("should not reach here")
        except ValidationError as error:
            self.assertTrue(
                "no more than 1" in error.message_dict['boot_size'][0]
            )

    def test_wear_status_invalid(self):
        try:
            Equipment(
                profile_id=self.tyler,
                title="Burton Legion Snowboard",
                price=Decimal('22'),
                equipment_product_name="Burton Legion Snowboard",
                bindings_product_name="Burton Legion Bindings",
                boots_product_name="Burton Gravity Boots",
                equipment_height=Decimal('70'),
                boot_size=Decimal('9.0'),
                wear_status="Bad",
            ).full_clean()
            self.fail("should not reach here")
        except ValidationError as error:
            self.assertTrue(
                "not a valid choice" in error.message_dict['wear_status'][0]
            )

    def test_equipment_type_invalid(self):
        try:
            Equipment(
                profile_id=self.tyler,
                title="Burton Legion Snowboard",
                price=Decimal('22'),
                equipment_product_name="Burton Legion Snowboard",
                bindings_product_name="Burton Legion Bindings",
                boots_product_name="Burton Gravity Boots",
                equipment_height=Decimal('70'),
                boot_size=Decimal('9.0'),
                equipment_type="Skateboard"
            ).full_clean()
            self.fail("should not reach here")
        except ValidationError as error:
            self.assertTrue(
                "not a valid choice" in error.message_dict['equipment_type'][0]
            )


class EquipmentListingTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(
            username="ty",
            email="ty@gmail.com",
            first_name="Tyler",
            last_name="Lo",
        )
        self.tyler = Profile.objects.create(
            user=self.user,
            first_name='Tyler',
            last_name='Lo',
            neighborhood='Shadyside',
            height=Decimal('5.6'),
            gender='Male',
            boot_size=9.0,
            user_type='Ski',
            phone_number='+1 (922) 282 1923'
        )
        self.tyler_board = Equipment.objects.create(
            profile_id=self.tyler,
            title="Burton Legion Snowboard",
            description="Nice Board",
            price=Decimal('22'),
            equipment_product_name="Burton Legion Snowboard",
            bindings_product_name="Burton Legion Bindings",
            boots_product_name="Burton Gravity Boots",
            skill_level='Advanced',
            equipment_height=Decimal('70'),
            boot_size=Decimal('9.0'),
            wear_status='Minimal-Wear',
            equipment_type='Snowboard',
        )

    def test_valid_equipment_listing(self):
        start = timezone.now() + timezone.timedelta(minutes=1)
        end = start + timezone.timedelta(days=60)
        listing = EquipmentListing(
            equipment_id=self.tyler_board,
            profile_id=self.tyler,
            start_date=start,
            end_date=end,
        )
        listing.full_clean()
        listing.save()
        self.assertEqual(listing.equipment_id.title, 'Burton Legion Snowboard')
        self.assertEqual(listing.profile_id.first_name, 'Tyler')
        self.assertEqual(listing.start_date, start)
        self.assertEqual(listing.end_date, end)

    def test_start_date_invalid(self):
        try:
            end = timezone.now() + timezone.timedelta(minutes=1)
            EquipmentListing(
                equipment_id=self.tyler_board,
                profile_id=self.tyler,
                start_date="foo",
                end_date=end,
            ).full_clean()
            self.fail("should not reach here")
        except ValidationError as error:
            self.assertTrue(
                "must be in YYYY-MM-DD"
                in
                error.message_dict['start_date'][0]
            )

    def test_end_date_invalid(self):
        try:
            start = timezone.now() + timezone.timedelta(minutes=1)
            EquipmentListing(
                equipment_id=self.tyler_board,
                profile_id=self.tyler,
                start_date=start,
                end_date="foo",
            ).full_clean()
            self.fail("should not reach here")
        except ValidationError as error:
            self.assertTrue(
                "must be in YYYY-MM-DD" in error.message_dict['end_date'][0]
            )

    def test_start_date_in_past(self):
        try:
            start = timezone.now() - timezone.timedelta(minutes=1)
            end = start + timezone.timedelta(days=60)
            EquipmentListing(
                equipment_id=self.tyler_board,
                profile_id=self.tyler,
                start_date=start,
                end_date=end,
            ).full_clean()
            self.fail("should not reach here")
        except ValidationError as error:
            self.assertTrue(
                "greater than or equal to current date"
                in
                error.message_dict['start_date'][0]
            )

    def test_end_date_before_start(self):
        try:
            start = timezone.now() + timezone.timedelta(minutes=1)
            EquipmentListing(
                equipment_id=self.tyler_board,
                profile_id=self.tyler,
                start_date=start,
                end_date=start,
            ).full_clean()
            self.fail("should not reach here")
        except ValidationError as error:
            self.assertTrue(
                "greater than the start date"
                in
                error.message_dict['__all__'][0]
            )


class EquipmentReservationTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(
            username="ty",
            email="ty@gmail.com",
            first_name="Tyler",
            last_name="Lo",
        )
        self.tyler = Profile.objects.create(
            user=self.user,
            first_name='Tyler',
            last_name='Lo',
            neighborhood='Shadyside',
            height=Decimal('5.6'),
            gender='Male',
            boot_size=9.0,
            user_type='Ski',
            phone_number='+1 (922) 282 1923'
        )
        self.tyler_board = Equipment.objects.create(
            profile_id=self.tyler,
            title="Burton Legion Snowboard",
            description="Nice Board",
            price=Decimal('22'),
            equipment_product_name="Burton Legion Snowboard",
            bindings_product_name="Burton Legion Bindings",
            boots_product_name="Burton Gravity Boots",
            skill_level='Advanced',
            equipment_height=Decimal('70'),
            boot_size=Decimal('9.0'),
            wear_status='Minimal-Wear',
            equipment_type='Snowboard',
        )

    def test_valid_equipment_reservation(self):
        start = timezone.now() + timezone.timedelta(minutes=1)
        end = start + timezone.timedelta(days=60)
        reservation = EquipmentReservation(
            equipment_id=self.tyler_board,
            profile_id=self.tyler,
            start_date=start,
            end_date=end,
        )
        reservation.full_clean()
        reservation.save()
        self.assertEqual(reservation.equipment_id.title,
                         'Burton Legion Snowboard')
        self.assertEqual(reservation.profile_id.first_name, 'Tyler')
        self.assertEqual(reservation.start_date, start)
        self.assertEqual(reservation.end_date, end)

    def test_start_date_invalid(self):
        try:
            end = timezone.now() + timezone.timedelta(minutes=1)
            EquipmentReservation(
                equipment_id=self.tyler_board,
                profile_id=self.tyler,
                start_date="foo",
                end_date=end,
            ).full_clean()
            self.fail("should not reach here")
        except ValidationError as error:
            self.assertTrue(
                "must be in YYYY-MM-DD" in error.message_dict['start_date'][0]
            )

    def test_end_date_invalid(self):
        try:
            start = timezone.now() + timezone.timedelta(minutes=1)
            EquipmentReservation(
                equipment_id=self.tyler_board,
                profile_id=self.tyler,
                start_date=start,
                end_date="foo",
            ).full_clean()
            self.fail("should not reach here")
        except ValidationError as error:
            self.assertTrue(
                "must be in YYYY-MM-DD" in error.message_dict['end_date'][0]
            )

    def test_start_date_in_past(self):
        try:
            start = timezone.now() - timezone.timedelta(minutes=1)
            end = start + timezone.timedelta(days=60)
            EquipmentReservation(
                equipment_id=self.tyler_board,
                profile_id=self.tyler,
                start_date=start,
                end_date=end,
            ).full_clean()
            self.fail("should not reach here")
        except ValidationError as error:
            self.assertTrue(
                "greater than or equal to current date"
                in
                error.message_dict['start_date'][0]
            )

    def test_end_date_before_start(self):
        try:
            start = timezone.now() + timezone.timedelta(minutes=1)
            EquipmentReservation(
                equipment_id=self.tyler_board,
                profile_id=self.tyler,
                start_date=start,
                end_date=start,
            ).full_clean()
            self.fail("should not reach here")
        except ValidationError as error:
            self.assertTrue(
                "greater than the start date"
                in
                error.message_dict['__all__'][0]
            )
