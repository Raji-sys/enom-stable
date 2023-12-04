from datetime import date
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Profile

class ProfileModelTest(TestCase):
    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(
            username='raji',
            password='8080mali',
            first_name='Muhammad Raji',
            last_name='Sunusi'
        )

    def test_profile_creation(self):
        # Ensure that a Profile instance is created when a user is created
        self.assertEqual(Profile.objects.count(), 0)

        # Create a Profile instance associated with the user
        profile = Profile.objects.create(
            user=self.user,
            email='rajisunusi@gmail.com',
            dob='1991-05-05',  # Set a valid date of birth for testing
            # Add other required fields here for a valid Profile instance
        )

        # Check that the Profile instance is created successfully
        self.assertEqual(Profile.objects.count(), 1)
        self.assertEqual(profile.user, self.user)
        self.assertEqual(profile.email, 'rajisunusi@gmail.com')
        self.assertEqual(profile.file_no, 6016)
        self.assertEqual(profile.title, 'mr')
        self.assertEqual(profile.gender, 'MALE')
        self.assertEqual(profile.dob, '1991-05-05')
        self.assertEqual(profile.phone, 9061267856 )
        self.assertEqual(profile.marital_status, 'SINGLE')
        self.assertEqual(profile.place_of_birth, 'Abuja' )
        self.assertEqual(profile.nationality, 'NIGERIAN' )
        self.assertEqual(profile.zone, 'NORTH-EAST')
        self.assertEqual(profile.state, 'Kano')
        self.assertEqual(profile.lga, 'Kano-Municipal')
        self.assertEqual(profile.sen_dist, 'Kano-central')
        self.assertEqual(profile.res_add, 'no 8 Panama Street Maitama Abuja')
        self.assertEqual(profile.per_res_addr, 'no 8 Panama Street Maitama Abuja' )
        self.assertEqual(profile.spouse, 'unknowm' )
        self.assertEqual(profile.hobbies, 'reading, football, chess, travelling')
        self.assertEqual(profile.religion,'ISLAM' )
        self.assertEqual(profile.qual, 'Degree' )
        self.assertEqual(profile.nofc, '3' )
        self.assertEqual(profile.nameoc, 'Muhammad, Ismail, Fatima' )
        self.assertEqual(profile.doboc, '2024-12-31', '2027-07-07', '2031-05-05' )
        self.assertEqual(profile.fnok_name, 'MS' )
        self.assertEqual(profile.fnok_no, 8079399390 )
        self.assertEqual(profile.fnok_email, 'ms@yahoo.com' )
        self.assertEqual(profile.fnok_addr, 'zawaciki kano' )
        self.assertEqual(profile.fnok_rel, 'Brother' )
        self.assertEqual(profile.snok_name, 'SMS' )
        self.assertEqual(profile.snok_no, 8079399390 )
        self.assertEqual(profile.snok_email, 'sms@gmail.com' )
        self.assertEqual(profile.snok_addr, 'east bye pass kano' )
        self.assertEqual(profile.snok_rel, 'Brother' )

    def test_profile_age(self):
        # Ensure that the age() method returns the correct age
        profile = Profile.objects.create(
            user=self.user,
            dob='1991-05-05',  # Set a valid date of birth for testing
            # Add other required fields here for a valid Profile instance
        )

        # Check that the age() method returns the correct age
        self.assertEqual(profile.age(), 32)
        # Replace expected_age with the expected age based on the provided date of birth

    def test_is_birthday(self):
        # Ensure that the is_birthday() method returns True on the user's birthday
        profile = Profile.objects.create(
            user=self.user,
            dob='1991-05-05',  # Set a valid date of birth for testing
            # Add other required fields here for a valid Profile instance
        )

        # Check that the is_birthday() method returns True on the user's birthday
        self.assertTrue(profile.is_birthday())

    # Add more test methods as needed for other functionalities in your Profile model
