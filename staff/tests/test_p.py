from datetime import date
from django.test import TestCase
from django.contrib.auth.models import User
from ..models import *
from django.utils import timezone
from datetime import timedelta


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
