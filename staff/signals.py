from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import *


@receiver(pre_save, sender=GovernmentAppointment)
def ret(sender, instance, **kwargs):
    today = date.today()
    age_at_retirement = instance.user.profile.age()
    years_of_service = today.year - instance.date_fapt.year if instance.date_fapt else None

    if instance.retire and instance.cleared:
        instance.retire = False
        instance.rtb = None
        return
    
    if instance.cleared:
        instance.retire=False
        instance.rtb = None
        return
    
    if instance.retire:
        instance.cleared=False
        return

    if age_at_retirement is not None and age_at_retirement >= 65:
        instance.retire = True
        instance.rtb = "RETIRE BY DATE OF BIRTH"

    elif years_of_service is not None and years_of_service >= 35:
        instance.retire = True
        instance.rtb = "RETIRE BY DATE OF APPOINTMENT"
    else:
        instance.retire = False


def update_govapp_on_retirement(sender, instance, **kwargs):
    if instance.retire:
        user = instance.user
        gov_app = instance.user.governmentappointment
        if gov_app:
            gov_app.retire = False
            gov_app.save()
            print(gov_app.retire)


@receiver(post_save, sender=GovernmentAppointment)
def increment_step(sender, instance, **kwargs):
    today = date.today()
    if today.month == 1 and today.day == 1 and instance.step is None:
        instance.step = instance.step + 1 if instance.step is not None else 1
        instance.save()

@receiver(post_save, sender=Promotion)
def update_govapp(sender, instance, **kwargs):
    gov_appointment = instance.user.governmentappointment
    gov_appointment.cpost = instance.cpost
    gov_appointment.save()


@receiver(post_save, sender=ExecutiveAppointment)
def update_govapp(sender, instance, **kwargs):
    gov_app = instance.user.governmentappointment if instance.user else None
    if gov_app:
        gov_app.cpost = instance.designation
        gov_app.save()