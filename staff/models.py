from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import timedelta, date
from django.db import models 
from django.urls import reverse
from django.contrib import messages
from django.utils.translation import gettext as _
from django.utils import timezone
from datetime import datetime

    
class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    middle_name=models.CharField(max_length=300, blank=True, null=True)
    email=models.EmailField(blank=True, null=True, max_length=100, unique=True)
    photo = models.ImageField(null=True,blank=True)
    file_no = models.DecimalField('file number', max_digits=6, decimal_places=0, null=True, unique=True, blank=False)
    title = models.CharField(max_length=300, null=True, blank=True)
    sex=(('MALE','MALE'),('FEMALE','FEMALE'))
    gender = models.CharField(choices=sex, max_length=10, null=True, blank=True)
    dob = models.DateField('date of birth',null=True, blank=True)
    phone = models.PositiveIntegerField(null=True, blank=True, unique=True)
    m_status=(('MARRIED','MARRIED'), ('SINGLE','SINGLE'), ('DIVORCED','DIVORCED'), ('DIVORCEE','DIVORCEE'), ('WIDOW','WIDOW'), ('WIDOWER','WIDOWER'))
    marital_status = models.CharField(choices=m_status, max_length=100, null=True, blank=True)
    place_of_birth = models.CharField(max_length=150, null=True, blank=True)
    ns=(('NIGERIAN','NIGERIAN'),('NON-CITIZEN','NON-CITIZEN'))   
    nationality = models.CharField(choices=ns, max_length=200, null=True, blank=True)
    geo_political_zone=(('NORTH-EAST','NORTH-EAST'),('NORTH-WEST','NORTH-WEST'),('NORTH-CENTRAL','NORTH-CENTRAL'),
                        ('SOUTH-EAST','SOUTH-EAST'),('SOUTH-WEST','SOUTH-WEST'),('SOUTH-SOUTH','SOUTH-SOUTH')) 
    zone = models.CharField(blank=True, choices=geo_political_zone, max_length=300, null=True)
    state=models.CharField(blank=True,max_length=300, null=True)
    lga=models.CharField(blank=True,max_length=300, null=True)
    sen_dist = models.CharField('senatorial district',max_length=300, null=True, blank=True)
    res_add = models.CharField('residential address',max_length=300, null=True, blank=True)
    per_res_addr = models.CharField('permanent residential address',max_length=300, null=True, blank=True)
    spouse = models.CharField(max_length=300, null=True, blank=True)
    hobbies = models.CharField(max_length=300, null=True, blank=True)
    faith=(('ISLAM', 'ISLAM'), ('CHRISTIANITY','CHRISTIANITY'),('TRADITIONAL', 'TRADITIONAL'))
    religion = models.CharField(choices=faith, max_length=100, null=True, blank=True)
    qual=models.CharField(max_length=150, null=True,blank=True)
    nofc = models.PositiveIntegerField('number of children',null=True, blank=True)
    nameoc = models.TextField('name of children',max_length=400, null=True, blank=True)
    doboc = models.TextField('date of birth of children',max_length=300, null=True, blank=True)
    fnok_name = models.CharField('first next of kin name',max_length=300, null=True, blank=True)
    fnok_phone = models.PositiveIntegerField('first next of kin phone',null=True, blank=True)
    fnok_email = models.EmailField('first next of kin email',max_length=300, null=True, blank=True)
    fnok_addr = models.CharField('first next of kin address',max_length=300, null=True, blank=True)
    fnok_rel = models.CharField('relationship with first next of kin', max_length=300, null=True, blank=True)
    fnok_photo = models.ImageField(null=True,blank=True)
    snok_name = models.CharField('second next of kin name', max_length=300, null=True, blank=True)
    snok_phone = models.PositiveIntegerField('second next of kin phone', null=True, blank=True)
    snok_email = models.EmailField('second next of kin email', max_length=300, null=True, blank=True)
    snok_addr = models.CharField('second next of address', max_length=300, null=True, blank=True)
    snok_rel = models.CharField('second next of kin', max_length=300, null=True, blank=True)
    snok_photo = models.ImageField(null=True,blank=True)
    created = models.DateTimeField('date added', auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('profile_details', args=[self.user])

    def full_name(self):
        return f"{self.user.get_full_name()}, {self.file_no}, {self.user.id}"
    
    def __str__(self):
        return self.user.username

    def age(self):
        today = date.today()
        if self.dob:
            age = today.year - self.dob.year

            if today.month < self.dob.month or (today.month == self.dob.month and today.day < self.dob.day):
                age -= 1
            return age
    
    def is_birthday(self):
        today = date.today()
        if self.dob:
            return today.month == self.dob.month and today.day == self.dob.day
        return False


class Qualification(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='qual')
    school = models.CharField(max_length=300, null=True, blank=True)
    types = (('PRIMARY', 'PRIMARY'), ('SECONDARY', 'SECONDARY'), ('COLLEGE OF EDUCATION', 'COLLEGE OF EDUCATION'),
             ('POLYTECHNIC', 'POLYTECHNIC'), ('UNIVERSITY', 'UNIVERSITY'))
    school_category = models.CharField(choices=types, max_length=300, null=True, blank=True)
    qual = models.CharField('qualification', max_length=300, null=True, blank=True)
    date_obtained = models.DateField(null=True, blank=True)
    created = models.DateTimeField('date added', auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('qual_details', args=[self.user])

    def __str__(self):
        if self.user:
            return f"{self.user.first_name} {self.user.last_name} - {self.qual}"


class ProfessionalQualification(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='pro_qual')
    institute = models.CharField(max_length=300, null=True, blank=True)
    inst_address = models.CharField('institute address', null=True, max_length=300, blank=True)
    qual_obtained = models.CharField('qualification obtained', null=True, max_length=300, blank=True)
    date_obtained = models.DateField(null=True, blank=True)
    created = models.DateTimeField('date added', auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
   
    def get_absolute_url(self):
        return reverse('pro_qual_details', args=[self.user])

    def __str__(self):
        if self.user:
            return f"{self.user.first_name} {self.user.last_name} - {self.qual_obtained}"


class GovernmentAppointment(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    dep=(
         ('ADMINISTRATION','ADMINISTRATION'),
         ('ACCOUNT','ACCOUNT'),
         ('BIO-MEDICAL ENGINEERING','BIO-MEDICAL ENGINEERING'),
         ('CLINICAL SERVICES','CLINICAL SERVICES'),
         ('CATERING','CATERING'),
         ('DISCIPLINE','DISCIPLINE'),
         ('ENGINEERING','ENGINEERING'),
         ('INFORMATION TECHNOLOGY','INFORMATION TECHNOLOGY'),
         ('INTERNAL AUDIT','INTERNAL AUDIT'),
         ('LEGAL','LEGAL'),
         ('LIBRARY','LIBRARY'),
         ('MEDICAL RECORD','MEDICAL RECORD'),
         ('MEDICAL ILLUSTRATION','MEDICAL ILLUSTRATION'),
         ('NURSING EDUCATION','NURSING EDUCATION'),
         ('NURSING SERVICES','NURSING SERVICES'),
         ('PATHOLOGY','PATHOLOGY'),
         ('PHARMACY','PHARMACY'),
         ('PHYSIOTHERAPHY','PHYSIOTHERAPHY'),
         ('PROSTHETIC AND ORTHOTICS','PROSTHETIC AND ORTHOTICS'),
         ('PROCUMENT','PROCUMENT'),
         ('PUBLIC HEALTH','PUBLIC HEALTH'),
         ('OCCUPATIONAL THERAPHY','OCCUPATIONAL THERAPHY'),
         ('RADIOLOGY','RADIOLOGY'),
         ('SERVICOM','SERVICOM'),
         ('SOCIAL WELFARE','SOCIAL WELFARE'),
         ('STORE','STORE'),
         ('TELEPHONE','TELEPHONE'),
         ('TRANSPORT','TRANSPORT'),
         )
    department=models.CharField(choices=dep, blank=True,max_length=300, null=True)
    cpost=models.CharField('current post',blank=True,max_length=300, null=True)
    ippis_no = models.DecimalField('IPPIS number', max_digits=6, decimal_places=0, null=True, unique=True, blank=True)
    date_fapt = models.DateField('date of first appointment', null=True,blank=True)
    date_capt = models.DateField('date of current appointment', null=True,blank=True)
    tp=(('CASUAL','CASUAL'),('LOCUM','LOCUM'),('PERMANENT','PERMANENT'),('PROBATION', 'PROBATION'))
    type_of_appt=models.CharField('type of appointment', choices=tp, null=True,max_length=300,blank=True)
    sfapt = models.FloatField('salary_per_annum_at_date_of_first_appointment', null=True,max_length=300,blank=True)    
    ss=(('CONHESS','CONHESS'),('CONMESS','CONMESS'), ('GIPMIS','GIPMIS'))
    salary_scale = models.CharField(choices=ss, null=True,max_length=300,blank=True)    
    gl=(('03','03'),('04','04'),('05','05'),('06','06'),('07','07'),('08','08'),('09','09'),
        ('11','11'),('12','12'),('13','13'),('14','14'),('15','15'))
    grade_level = models.CharField(choices=gl, null=True,max_length=300,blank=True)
    step = models.PositiveIntegerField(null=True, blank=True)
    tc=(('JUNIOR','JUNIOR'), ('SENIOR','SENIOR'),('EXECUTIVE','EXECUTIVE'))
    type_of_cadre=models.CharField(choices=tc, null=True, blank=True, max_length=100)
    exams_status = models.CharField(null=True, blank=True, max_length=100)
    created = models.DateTimeField('date added', auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('govapp_details', args=[self.user])

    def full_name(self):
        return f"{self.user.get_full_name()}, {self.cpost}"
    
    def __str__(self):
        return self.user.username


    def step_inc(self):
        today = date.today()
        if self.step is not None:
            if today.month == 1 and today.day == 1:
                self.step += 1
                self.save()
         

    def get_absolute_url(self):
        return reverse('prom_details', args=[self.user])

    def __str__(self):
        if self.user:
            return f"{self.user.last_name} {self.user.first_name}"

    #promotion calculation


class Promotion(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='promotion')
    cpost = models.CharField('current post', null=True, max_length=300, blank=True)
    govapp = models.ForeignKey(GovernmentAppointment, on_delete=models.CASCADE, related_name='progovapp')
    prom_date = models.DateField('promotion date', null=True, blank=True)
    gl = models.PositiveIntegerField('grade level', null=True, blank=True)
    step = models.PositiveIntegerField(null=True, blank=True)
    inc_date = models.DateField('increment date', null=True, blank=True)
    conf_date = models.DateField('confirmation date', null=True, blank=True)
    due = models.BooleanField(default=False)
    created = models.DateTimeField('date added', auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('prom_details', args=[self.user])

    def __str__(self):
        if self.user:
            return f"{self.user.last_name} {self.user.first_name}"

        # Promotion calculation
    def calculate_promotion(self):
        today = date.today()

        if self.govapp.date_capt:
            cal = self.govapp.date_capt.year
            ex = self.govapp.exams_status
            gl = self.govapp.grade_level
            tc = self.govapp.type_of_cadre

    # Performing checks
        if (
            (today.year - cal == 3 and int(gl) >= 6 and ex == 'pass' and tc == 'SENIOR') or
            (today.year - cal == 2 and int(gl) <= 5 and ex == 'pass' and tc == 'JUNIOR') or
            (today.year - cal == 4 and int(gl) >= 13 and ex == 'pass' and tc == 'EXECUTIVE')
            ):
            self.due = True
            self.save()
            return 'DUE FOR PROMOTION'

    # If not due, no need to send a message
        self.due = False
        self.save()
        return None


class Discipline(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='discipline')
    offense = models.TextField(null=True, blank=True)
    decision = models.TextField(null=True, blank=True)
    action_date = models.DateField('date of disciplinary action', null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    created = models.DateTimeField('date added', auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('dis_details', args=[self.user])

    class Meta:
        verbose_name_plural = 'Disciplinaries'
    
    def __str__(self):
        if self.user:
            return f"{self.user.last_name} {self.user.first_name}"


class Leave(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='leave')
    nature = models.CharField('nature of leave', null=True, max_length=300, blank=True)
    year = models.PositiveIntegerField(null=True, blank=True)
    start_date = models.DateField(null=True, blank=False)
    total_days = models.PositiveIntegerField(null=True, blank=True)
    balance = models.PositiveIntegerField(null=True, blank=True)
    granted = models.PositiveIntegerField('number of days granted', null=True, blank=False)
    status = models.CharField(null=True, max_length=300, blank=True)
    is_leave_over = models.BooleanField(default=False)
    comments = models.TextField('comments if any', null=True, blank=True)
    created = models.DateTimeField('date added', auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('lv_details', args=[self.user])

    def __str__(self):
        if self.user:
            return f"{self.user.last_name} {self.user.first_name}"

    def remain(self):
        if self.total_days is not None and self.granted is not None:
            return max(0, self.total_days - self.granted)

    def validate_leave(self):
        r = self.remain()
        if r is not None:
            if r < 0:
                raise ValidationError('Your leave is over.')
            elif self.granted == 0:
                raise ValidationError('No days are granted.')

    def save(self, *args, **kwargs):
        self.clean()
        self.validate_leave()
        super().save(*args, **kwargs)


    def return_on(self):
        if self.granted is not None and self.granted > 0:
            if isinstance(self.start_date, datetime):
                return (self.start_date + timedelta(days=self.granted)).date()
            else:
                return self.start_date + timedelta(days=self.granted)
        return None

    def over(self):
        return self.return_on() is not None and self.return_on() < timezone.now().date()
   

class ExecutiveAppointment(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='execapp')
    designation = models.CharField(null=True,max_length=300,blank=True)
    govapp=models.ForeignKey(GovernmentAppointment, on_delete=models.CASCADE, related_name='execgovapp')
    date = models.DateField(null=True,blank=True)
    status = models.CharField(null=True,max_length=300,blank=True)
    created = models.DateTimeField('date added', auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('exeapp_details', args=[self.user])
    
    def __str__(self):
        if self.user:
            return f"{self.user.last_name} {self.user.first_name}"


class Retirement(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    date = models.DateField(null=True,blank=True)
    govapp=models.ForeignKey(GovernmentAppointment, on_delete=models.CASCADE, related_name='rtgovapp')
    profile=models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='profile')
    status = models.CharField(null=True,max_length=300,blank=True)
    retire=models.BooleanField(null=True, blank=True)
    rtb=models.CharField('retired by', null=True, blank=True,max_length=50)
    created = models.DateTimeField('date added', auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('rt_details', args=[self.user])
    
    def __str__(self):
        if self.user:
            return f"{self.user.last_name} {self.user.first_name}"
    
    def rt(self):
        today = date.today()
        age_at_retirement = self.profile.age()
        years_of_service = today.year - self.govapp.date_fapt.year if self.govapp.date_fapt else None

        if age_at_retirement is not None and age_at_retirement >= 65:
            self.retire = True
            self.rtb = "RETIRE BY DATE OF BIRTH"
        elif years_of_service is not None and years_of_service >= 35:
            self.retire = True
            self.rtb = "RETIRE BY DATE OF APPOINTMENT"
        else:
            self.retire = False

        self.save()