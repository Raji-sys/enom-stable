from django.core.management.base import BaseCommand
from django.utils import timezone
from staff.models import GovernmentAppointment

class Command(BaseCommand):
    help = 'Increment steps for all government appointments'

    def handle(self, *args, **options):
        today = timezone.now().date()
        if today.month == 1 and today.day == 1:
            appointments = GovernmentAppointment.objects.all()
            for appointment in appointments:
                appointment.increment_step()
            self.stdout.write(self.style.SUCCESS(f'Successfully incremented steps for {appointments.count()} appointments'))
        else:
            self.stdout.write(self.style.WARNING('This command should only be run on January 1st'))