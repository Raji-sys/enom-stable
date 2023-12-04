from datetime import date
from django.test import TestCase
from django.contrib.auth.models import User
from ..models import *
from django.utils import timezone
from datetime import timedelta


class ProfileModelTest(TestCase):
    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(
            username='user-pro',
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
            file_no= 6016,
            title= 'mr',
            gender= 'MALE',
            phone= 9061267856 ,
            marital_status= 'SINGLE',
            place_of_birth= 'Abuja' ,
            nationality= 'NIGERIAN' ,
            zone= 'NORTH-EAST',
            state= 'Kano',
            lga= 'Kano-Municipal',
            sen_dist= 'Kano-central',
            res_add= 'no 8 Panama Street Maitama Abuja',
            per_res_addr= 'no 8 Panama Street Maitama Abuja',
            spouse= 'unknowm' ,
            hobbies= 'reading, football, chess, travelling',
            religion='ISLAM' ,
            qual= 'Degree' ,
            nofc= '3' ,
            nameoc= 'Muhammad, Ismail, Fatima' ,
            doboc= '2024-12-31, 2027-07-07, 2031-05-05',
            fnok_name= 'MS' ,
            fnok_phone= 8079399390 ,
            fnok_email= 'ms@yahoo.com' ,
            fnok_addr= 'zawaciki kano' ,
            fnok_rel= 'Brother' ,
            snok_name= 'SMS' ,
            snok_phone= 8079399390 ,
            snok_email= 'sms@gmail.com' ,
            snok_addr= 'east bye pass kano' ,
            snok_rel= 'Brother',
        )
            # Add other required fields here for a valid Profile instance
        

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
        self.assertEqual(profile.per_res_addr, 'no 8 Panama Street Maitama Abuja')
        self.assertEqual(profile.spouse, 'unknowm' )
        self.assertEqual(profile.hobbies, 'reading, football, chess, travelling')
        self.assertEqual(profile.religion,'ISLAM' )
        self.assertEqual(profile.qual, 'Degree' )
        self.assertEqual(profile.nofc, '3' )
        self.assertEqual(profile.nameoc, 'Muhammad, Ismail, Fatima' )
        self.assertEqual(profile.doboc, '2024-12-31, 2027-07-07, 2031-05-05')
        self.assertEqual(profile.fnok_name, 'MS' )
        self.assertEqual(profile.fnok_phone, 8079399390 )
        self.assertEqual(profile.fnok_email, 'ms@yahoo.com' )
        self.assertEqual(profile.fnok_addr, 'zawaciki kano' )
        self.assertEqual(profile.fnok_rel, 'Brother' )
        self.assertEqual(profile.snok_name, 'SMS' )
        self.assertEqual(profile.snok_phone, 8079399390 )
        self.assertEqual(profile.snok_email, 'sms@gmail.com' )
        self.assertEqual(profile.snok_addr, 'east bye pass kano' )
        self.assertEqual(profile.snok_rel, 'Brother' )

    def test_profile_age(self):
        dob = date(1991, 5, 5) 
        # Ensure that the age() method returns the correct age
        profile = Profile.objects.create(
            user=self.user,
            email='rajisunusi@gmail.com',
            dob=dob,  # Set a valid date of birth for testing
            file_no= 6016,
            title= 'mr',
            gender= 'MALE',
            phone= 9061267856 ,
            marital_status= 'SINGLE',
            place_of_birth= 'Abuja' ,
            nationality= 'NIGERIAN' ,
            zone= 'NORTH-EAST',
            state= 'Kano',
            lga= 'Kano-Municipal',
            sen_dist= 'Kano-central',
            res_add= 'no 8 Panama Street Maitama Abuja',
            per_res_addr= 'no 8 Panama Street Maitama Abuja',
            spouse= 'unknowm' ,
            hobbies= 'reading, football, chess, travelling',
            religion='ISLAM' ,
            qual= 'Degree' ,
            nofc= '3' ,
            nameoc= 'Muhammad, Ismail, Fatima' ,
            doboc= '2024-12-31, 2027-07-07, 2031-05-05',
            fnok_name= 'MS' ,
            fnok_phone= 8079399390 ,
            fnok_email= 'ms@yahoo.com' ,
            fnok_addr= 'zawaciki kano' ,
            fnok_rel= 'Brother' ,
            snok_name= 'SMS' ,
            snok_phone= 8079399390 ,
            snok_email= 'sms@gmail.com' ,
            snok_addr= 'east bye pass kano' ,
            snok_rel= 'Brother',
             # Set a valid date of birth for testing
            # Add other required fields here for a valid Profile instance
        )

        # Check that the age() method returns the correct age
        self.assertEqual(profile.age(), 32)
        # Replace expected_age with the expected age based on the provided date of birth

    def test_is_birthday(self):
        today = date.today()
        dob = date(today.year, today.month, today.day) 
        # Ensure that the is_birthday() method returns True on the user's birthday
        profile = Profile.objects.create(
            user=self.user,
            email='rajisunusi@gmail.com',
            dob=dob,  # Set a valid date of birth for testing
            file_no= 6016,
            title= 'mr',
            gender= 'MALE',
            phone= 9061267856 ,
            marital_status= 'SINGLE',
            place_of_birth= 'Abuja' ,
            nationality= 'NIGERIAN' ,
            zone= 'NORTH-EAST',
            state= 'Kano',
            lga= 'Kano-Municipal',
            sen_dist= 'Kano-central',
            res_add= 'no 8 Panama Street Maitama Abuja',
            per_res_addr= 'no 8 Panama Street Maitama Abuja',
            spouse= 'unknowm' ,
            hobbies= 'reading, football, chess, travelling',
            religion='ISLAM' ,
            qual= 'Degree' ,
            nofc= '3' ,
            nameoc= 'Muhammad, Ismail, Fatima' ,
            doboc= '2024-12-31, 2027-07-07, 2031-05-05',
            fnok_name= 'MS' ,
            fnok_phone= 8079399390 ,
            fnok_email= 'ms@yahoo.com' ,
            fnok_addr= 'zawaciki kano' ,
            fnok_rel= 'Brother' ,
            snok_name= 'SMS' ,
            snok_phone= 8079399390 ,
            snok_email= 'sms@gmail.com' ,
            snok_addr= 'east bye pass kano' ,
            snok_rel= 'Brother',
            # Add other required fields here for a valid Profile instance
        )

        # Check that the is_birthday() method returns True on the user's birthday
        self.assertTrue(profile.is_birthday())


class QualificationModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='user-qual', password='8080mali')

    def test_qualification_creation(self):
        qualification = Qualification.objects.create(
            user=self.user,
            school='Mahatma Gandhi University',
            school_category='UNIVERSITY',
            qual='Bsc Information Technology',
            date_obtained=date(2018, 4, 16)
        )
        self.assertEqual(qualification.user, self.user)
        self.assertEqual(qualification.school, 'Mahatma Gandhi University')
        self.assertEqual(qualification.school_category, 'UNIVERSITY')
        self.assertEqual(qualification.qual, 'Bsc Information Technology')
        self.assertEqual(qualification.date_obtained, date(2018, 4, 16))

class ProfessionalQualificationModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='user-proqual', password='8080mali')

    def test_professional_qualification_creation(self):
        prof_qualification = ProfessionalQualification.objects.create(
            user=self.user,
            institute='La Daght',
            inst_address='lorem testing la dahgt 11 street',
            qual_obtained='Certificate',
            date_obtained=date(2020, 1, 5)
        )
        self.assertEqual(prof_qualification.user, self.user)
        self.assertEqual(prof_qualification.institute, 'La Daght')
        self.assertEqual(prof_qualification.inst_address, 'lorem testing la dahgt 11 street')
        self.assertEqual(prof_qualification.qual_obtained, 'Certificate')
        self.assertEqual(prof_qualification.date_obtained, date(2020, 1, 5))


class GovernmentAppointmentModelTest(TestCase):
    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create(username='user-govapp', password='8080mali')

        # Create a GovernmentAppointment instance for testing
        self.gov_appointment = GovernmentAppointment.objects.create(
            user=self.user,
            department='ADMINISTRATION',
            cpost='Test Post',
            ippis_no=123456,
            date_fapt='2020-01-01',
            date_capt='2022-01-01',
            type_of_appt='PERMANENT',
            sfapt=50000.0,
            salary_scale='CONHESS',
            grade_level='08',
            step=3,
            type_of_cadre='SENIOR',
            exams_status='PASS',
        )

    def test_step_inc(self):
        # Get the initial step value
        initial_step = self.gov_appointment.step

        # Call the step_inc method
        self.gov_appointment.step_inc()

        # Get the updated step value
        updated_step = GovernmentAppointment.objects.get(id=self.gov_appointment.id).step

        # Check if the step has increased by 1
        self.assertEqual(updated_step, initial_step + 1)


class PromotionModelTest(TestCase):
    def setUp(self):
        # Create a common user for some scenarios
        self.common_user = User.objects.create_user(username='common_user', password='8080mali')

    def test_calculate_promotion_due_senior_pass_grade_range(self):
        # Test for grade levels 6 to 12
        for grade_level in range(6, 13):
            # Create a unique user for each iteration using grade_level in the username
            user = User.objects.create_user(username=f'user_grade_{grade_level}', password='password')

            # Create a GovernmentAppointment with conditions for due promotion
            govapp = GovernmentAppointment.objects.create(
                user=user,
                date_capt=timezone.now().date() - timedelta(days=3 * 365),
                exams_status='pass',
                grade_level=str(grade_level),
                type_of_cadre='SENIOR',
            )
            promotion = Promotion.objects.create(user=user, govapp=govapp)

            # Call calculate_promotion
            result = promotion.calculate_promotion()

            # Check if promotion is due
            self.assertTrue(promotion.due)
            # Check if success message is returned
            self.assertEqual(result, 'DUE FOR PROMOTION')

    def test_calculate_promotion_not_due_senior_fail_grade_range(self):
        # Test for grade levels outside the range 6 to 12
        for grade_level in range(1, 6):
            # Create a unique user for each iteration using grade_level in the username
            user = User.objects.create_user(username=f'user_grade_{grade_level}', password='password')

            # Create a GovernmentAppointment with conditions for not due promotion
            govapp = GovernmentAppointment.objects.create(
                user=user,
                date_capt=timezone.now().date() - timedelta(days=3 * 365),
                exams_status='fail',  # Assuming fail means not eligible for promotion
                grade_level=str(grade_level),
                type_of_cadre='SENIOR',
            )
            promotion = Promotion.objects.create(user=user, govapp=govapp)

            # Call calculate_promotion
            result = promotion.calculate_promotion()

            # Check if promotion is not due
            self.assertFalse(promotion.due)
            # Check if success message is not returned
            self.assertIsNone(result)

    def test_calculate_promotion_due_junior_pass_grade_range(self):
        for grade_level in range(1, 6):
        # Create a unique username for each iteration
            username = f'user_promotion_due_junior_grade_{grade_level}'
            user = User.objects.create_user(username=username, password='8080mali')

        # Create a GovernmentAppointment with conditions for due promotion
        govapp = GovernmentAppointment.objects.create(
            user=user,
            date_capt=timezone.now().date() - timedelta(days=2 * 365),
            exams_status='pass',
            grade_level=str(grade_level),
            type_of_cadre='JUNIOR',
        )
        promotion = Promotion.objects.create(user=user, govapp=govapp)

        result = promotion.calculate_promotion()

        self.assertTrue(promotion.due)
        self.assertEqual(result, 'DUE FOR PROMOTION')


    def test_calculate_promotion_not_due_junior_fail_grade_range(self):
        for grade_level in range(6, 13):
            # Create a unique username for each iteration
            username = f'user_promotion_not_due_junior_grade_{grade_level}'
            user = User.objects.create_user(username=username, password='8080mali')

            # Create a GovernmentAppointment with conditions for not due promotion
            govapp = GovernmentAppointment.objects.create(
                user=user,
                date_capt=timezone.now().date() - timedelta(days=2 * 365),
                exams_status='fail',
                grade_level=str(grade_level),
                type_of_cadre='JUNIOR',
            )
            promotion = Promotion.objects.create(user=user, govapp=govapp)

            result = promotion.calculate_promotion()

            self.assertFalse(promotion.due)
            self.assertIsNone(result)


    def test_calculate_promotion_due_executive_pass_grade_range(self):
        for grade_level in range(13, 16):
            # Create a unique username for each iteration
            username = f'user_promotion_due_executive_grade_{grade_level}'
            user = User.objects.create_user(username=username, password='8080mali')

            # Create a GovernmentAppointment with conditions for due promotion
            govapp = GovernmentAppointment.objects.create(
                user=user,
                date_capt=timezone.now().date() - timedelta(days=4 * 365),
                exams_status='pass',
                grade_level=str(grade_level),
                type_of_cadre='EXECUTIVE',
            )
            promotion = Promotion.objects.create(user=user, govapp=govapp)

            result = promotion.calculate_promotion()

            self.assertTrue(promotion.due)
            self.assertEqual(result, 'DUE FOR PROMOTION')


    def test_calculate_promotion_not_due_executive_fail_grade_range(self):
        for grade_level in range(1, 13):
            # Create a unique username for each iteration
            username = f'user_promotion_not_due_executive_grade_{grade_level}'
            user = User.objects.create_user(username=username, password='8080mali')

            # Create a GovernmentAppointment with conditions for not due promotion
            govapp = GovernmentAppointment.objects.create(
                user=user,
                date_capt=timezone.now().date() - timedelta(days=4 * 365),
                exams_status='fail',
                grade_level=str(grade_level),
                type_of_cadre='EXECUTIVE',
            )
            promotion = Promotion.objects.create(user=user, govapp=govapp)

            result = promotion.calculate_promotion()

            self.assertFalse(promotion.due)
            self.assertIsNone(result)
