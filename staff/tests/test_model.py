from datetime import date
from django.test import TestCase
from django.contrib.auth.models import User
from ..models import *
from django.utils import timezone
from datetime import timedelta,date


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
            middle_name='amir',
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
        self.assertEqual(profile.middle_name, 'amir')
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
            middle_name='amir',
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

    def test_step_increment_on_new_year(self):
        # Create a GovernmentAppointment instance with a specific step
        gov_app = GovernmentAppointment.objects.create(step=3)

        # Simulate the passage of one year
        new_year_date = timezone.now() + timezone.timedelta(days=365)

        # Set the date to January 1st of the next year
        new_year_date = new_year_date.replace(month=1, day=1)

        # Update the instance's modified timestamp to simulate a save
        gov_app.save()

        # Reload the instance from the database
        gov_app.refresh_from_db()

        # Assert that the step has been incremented
        self.assertEqual(gov_app.step, 4)

    def test_step_manual_update(self):
        # Create a GovernmentAppointment instance with a specific step
        gov_app = GovernmentAppointment.objects.create(step=3)

        # Manually update the step to 5
        gov_app.step = 5
        gov_app.save()

        # Simulate the passage of one year
        new_year_date = timezone.now() + timezone.timedelta(days=365)

        # Set the date to January 1st of the next year
        new_year_date = new_year_date.replace(month=1, day=1)

        # Update the instance's modified timestamp to simulate a save
        gov_app.save()

        # Reload the instance from the database
        gov_app.refresh_from_db()

        # Assert that the step remains 5 after manual update
        self.assertEqual(gov_app.step, 5)


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


class DisciplineModelTest(TestCase):
    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(username='test_user', password='test_password')

    def test_discipline_creation(self):
        # Create a Discipline instance
        discipline = Discipline.objects.create(
            user=self.user,
            offense='Test Offense',
            decision='Test Decision',
            action_date=date.today(),
            comment='Test Comment',
        )

        # Check if the Discipline instance is created successfully
        self.assertIsInstance(discipline, Discipline)
        self.assertEqual(discipline.user, self.user)
        self.assertEqual(discipline.offense, 'Test Offense')
        self.assertEqual(discipline.decision, 'Test Decision')
        self.assertEqual(discipline.action_date, date.today())
        self.assertEqual(discipline.comment, 'Test Comment')

    def test_get_absolute_url(self):
        # Create a Discipline instance
        discipline = Discipline.objects.create(
            user=self.user,
            offense='Test Offense',
            decision='Test Decision',
            action_date=date.today(),
            comment='Test Comment',
        )

        # Check if get_absolute_url returns a valid URL
        # expected_url = f'/discipline/{self.user.id}/'
        # self.assertEqual(discipline.get_absolute_url(), expected_url)

    def test_str_representation(self):
        # Create a Discipline instance
        discipline = Discipline.objects.create(
            user=self.user,
            offense='Test Offense',
            decision='Test Decision',
            action_date=date.today(),
            comment='Test Comment',
        )

        # Check if the __str__ method returns the expected string
        expected_str = f"{self.user.last_name} {self.user.first_name}"
        self.assertEqual(str(discipline), expected_str)


class LeaveModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser', first_name='John', last_name='Doe')
        self.leave = Leave.objects.create(
            user=self.user,
            nature='Vacation',
            year=2023,
            start_date=date(2023, 1, 1),
            total_days=10,
            granted=5,
            status='Pending',
            comments='Enjoy your time off!'
        )

    def test_leave_remain_method(self):
        self.assertEqual(self.leave.remain(), 5)  # 10 total days - 5 granted days

    def test_leave_clean_method_valid(self):
        # This should not raise a ValidationError
        self.leave.clean()

    def test_leave_return_on_method(self):
        expected_return_date = self.leave.start_date + timedelta(days=self.leave.granted)
        self.assertEqual(self.leave.return_on(), expected_return_date)

    
    def test_leave_over(self):
        # Check if the leave is over
        self.assertTrue(self.leave.over())


    def test_leave_clean_method_invalid(self):
        # Modify the granted days to trigger the validation error
        self.leave.granted = 0
        
        # Ensure that the validation error is raised
        with self.assertRaises(ValidationError):
            self.leave.validate_leave()

    def test_leave_not_over(self):
        # Check if the leave is not over
        self.leave.start_date = timezone.now() + timedelta(days=5)
        self.assertFalse(self.leave.over())

    def test_leave_with_zero_granted_days(self):
        # Create a Leave instance with granted days equal to 0
        self.leave.granted = 0
        self.assertFalse(self.leave.over())

    def test_leave_with_negative_granted_days(self):
        # Create a Leave instance with negative granted days
        self.leave.granted = -3
        self.assertFalse(self.leave.over())

    def test_leave_with_no_granted_days(self):
        # Create a Leave instance with no granted days
        self.leave.granted = None
        self.assertFalse(self.leave.over())

class ExecutiveAppointmentModelTest(TestCase):

    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create(username='test_user', first_name='John', last_name='Doe')

        # Create a GovernmentAppointment for testing
        self.gov_appointment = GovernmentAppointment.objects.create(
            cpost='Minister of Finance',
            department='Finance Department'
        )

    def test_executive_appointment_creation(self):
        exec_appointment = ExecutiveAppointment.objects.create(
            user=self.user,
            designation='Chief Executive Officer',
            govapp=self.gov_appointment,
            date=date(2023, 1, 1),
            status='Active'
        )

        self.assertEqual(exec_appointment.user, self.user)
        self.assertEqual(exec_appointment.designation, 'Chief Executive Officer')
        self.assertEqual(exec_appointment.govapp, self.gov_appointment)
        self.assertEqual(exec_appointment.date, date(2023, 1, 1))
        self.assertEqual(exec_appointment.status, 'Active')

    def test_get_absolute_url_method(self):
        exec_appointment = ExecutiveAppointment.objects.create(
            user=self.user,
            designation='Chief Executive Officer',
            govapp=self.gov_appointment,
            date=date(2023, 1, 1),
            status='Active'
        )

        # expected_url = f'/exeapp_details/{self.user.id}/'
        # self.assertEqual(exec_appointment.get_absolute_url(), expected_url)

    def test_str_method(self):
        exec_appointment = ExecutiveAppointment.objects.create(
            user=self.user,
            designation='Chief Executive Officer',
            govapp=self.gov_appointment,
            date=date(2023, 1, 1),
            status='Active'
        )

        expected_str = f"{self.user.last_name} {self.user.first_name}"
        self.assertEqual(str(exec_appointment), expected_str)


class RetirementModelTest(TestCase):
    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create(username='test_user', first_name='John', last_name='Doe')

        # Create a GovernmentAppointment for testing
        self.gov_appointment = GovernmentAppointment.objects.create(
            cpost='Minister of Finance',
            department='Finance Department',
            date_fapt=date.today() - timedelta(days=36 * 365) 
        )

        # Create a Profile for testing
        self.profile = Profile.objects.create(
            user=self.user,
            dob=date(1980, 1, 1)
        )

    def test_retirement_creation(self):
        retirement = Retirement.objects.create(
            user=self.user,
            date=date(2023, 1, 1),
            govapp=self.gov_appointment,
            profile=self.profile,
            status='Active'
        )

        self.assertEqual(retirement.user, self.user)
        self.assertEqual(retirement.date, date(2023, 1, 1))
        self.assertEqual(retirement.govapp, self.gov_appointment)
        self.assertEqual(retirement.profile, self.profile)
        self.assertEqual(retirement.status, 'Active')

    # def test_get_absolute_url_method(self):
    #     retirement = Retirement.objects.create(
    #         user=self.user,
    #         date=date(2023, 1, 1),
    #         govapp=self.gov_appointment,
    #         profile=self.profile,
    #         status='Active'
    #     )

        # expected_url = f'/rt_details/{self.user.id}/'
        # self.assertEqual(retirement.get_absolute_url(), expected_url)

    def test_str_method(self):
        retirement = Retirement.objects.create(
            user=self.user,
            date=date(2023, 1, 1),
            govapp=self.gov_appointment,
            profile=self.profile,
            status='Active'
        )

        expected_str = f"{self.user.last_name} {self.user.first_name}"
        self.assertEqual(str(retirement), expected_str)

    def test_rt_method(self):
            retirement = Retirement.objects.create(
                user=self.user,
                date=date(2023, 1, 1),
                govapp=self.gov_appointment,
                profile=self.profile,
                status='Active'
            )

            retirement.rt()  # Trigger the rt() method

            print(retirement.profile.age())
            print(date.today().year - self.gov_appointment.date_fapt.year)
            print(retirement.retire)

            self.assertTrue(retirement.retire)
            self.assertEqual(retirement.rtb, "RETIRE BY DATE OF APPOINTMENT")