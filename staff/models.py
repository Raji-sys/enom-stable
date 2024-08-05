from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import timedelta, date
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _
from django.utils import timezone
from datetime import datetime



class Department(models.Model):
    name = models.CharField(max_length=200, unique=True,null=True, blank=True)
    head = models.CharField(max_length=200, unique=True,null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def user_count(self):
        return self.governmentappointment_set.count()
    
    def get_absolute_url(self):
        return reverse('department_details', args=[self.pk])

    def __str__(self):
        return self.name


class Duties(models.Model):
    name = models.CharField(max_length=200, unique=True,null=True, blank=True)
    department = models.ForeignKey(Department,blank=True, max_length=300, null=True,on_delete=models.CASCADE,related_name='dept_duties')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name_plural = 'Duties and responsibilities'
    
    def __str__(self):
        return self.name


class Post(models.Model):
    name = models.CharField(max_length=200, unique=True,null=True, blank=True)
    department = models.ForeignKey(Department,blank=True, max_length=300, null=True,on_delete=models.CASCADE,related_name='post_dept')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def user_count(self):
        return self.governmentappointment_set.count()
    
    def get_absolute_url(self):
        return reverse('post_details', args=[self.pk])

    def __str__(self):
        return self.name


class Zone(models.Model):
    name = models.CharField(max_length=200, unique=True,null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    
    def user_count(self):
        return self.governmentappointment_set.count()
    
    def get_absolute_url(self):
        return reverse('zone_details', args=[self.pk])

    def __str__(self):
        return self.name
    

class State(models.Model):
    name = models.CharField(max_length=200, unique=True,null=True, blank=True)
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now=True)
    
    def user_count(self):
        return self.governmentappointment_set.count()
    
    def get_absolute_url(self):
        return reverse('state_details', args=[self.pk])

    def __str__(self):
        return self.name


class LGA(models.Model):
    name = models.CharField(max_length=200, unique=True,null=True, blank=True)
    state = models.ForeignKey(State,blank=True, max_length=300, null=True,on_delete=models.CASCADE,related_name='lga_state')
    updated = models.DateTimeField(auto_now=True)
    
    def user_count(self):
        return self.governmentappointment_set.count()
    
    def get_absolute_url(self):
        return reverse('lga_details', args=[self.pk])

    def __str__(self):
        return self.name


class SenateDistrict(models.Model):
    name = models.CharField(max_length=200, unique=True,null=True, blank=True)
    lga = models.ForeignKey(LGA,blank=True, max_length=300, null=True,on_delete=models.CASCADE,related_name='senate_district_lga')
    updated = models.DateTimeField(auto_now=True)
    
    def user_count(self):
        return self.governmentappointment_set.count()
    
    def get_absolute_url(self):
        return reverse('senate_district_details', args=[self.pk])

    def __str__(self):
        return self.name


class SalaryScale(models.Model):
    name = models.CharField(max_length=200, unique=True,null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def user_count(self):
        return self.governmentappointment_set.count()
    
    def get_absolute_url(self):
        return reverse('salary_scale_details', args=[self.pk])

    def __str__(self):
        return self.name


class GradeLevel(models.Model):
    name = models.CharField(max_length=200, unique=True,null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def user_count(self):
        return self.governmentappointment_set.count()

    
    def get_absolute_url(self):
        return reverse('grade_level_details', args=[self.pk])

    def __str__(self):
        return self.name


class TypeOfCadre(models.Model):
    name = models.CharField(max_length=200, unique=True,null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def user_count(self):
        return self.governmentappointment_set.count()

    
    def get_absolute_url(self):
        return reverse('type_of_cadre_details', args=[self.pk])

    def __str__(self):
        return self.name


class TypeOfAppt(models.Model):
    name = models.CharField(max_length=200, unique=True,null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def user_count(self):
        return self.governmentappointment_set.count()

    
    def get_absolute_url(self):
        return reverse('type_of_appt_details', args=[self.pk])

    def __str__(self):
        return self.name


class LeaveTypes(models.Model):
    name = models.CharField(max_length=200, unique=True,null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural='type of leaves'

    def user_count(self):
        return self.governmentappointment_set.count()

    
    def get_absolute_url(self):
        return reverse('nature_of_leave_details', args=[self.pk])

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    middle_name = models.CharField(max_length=300, blank=True, null=True)
    email = models.EmailField(blank=True, null=True,max_length=100, unique=True)
    photo = models.ImageField(null=True, blank=True)
    file_no = models.DecimalField('file number', max_digits=6, decimal_places=0, null=True, unique=True, blank=True)
    title = models.CharField(max_length=300, null=True, blank=True)
    sex = (('MALE', 'MALE'), ('FEMALE', 'FEMALE'))
    gender = models.CharField(choices=sex, max_length=10, null=True, blank=True)
    dob = models.DateField('date of birth', null=True, blank=True)
    phone = models.PositiveIntegerField(null=True, blank=True, unique=True)

    m_status = (('MARRIED', 'MARRIED'), ('SINGLE', 'SINGLE'), ('DIVORCED', 'DIVORCED'),('DIVORCEE', 'DIVORCEE'), ('WIDOW', 'WIDOW'), ('WIDOWER', 'WIDOWER'))
    marital_status = models.CharField(choices=m_status, max_length=100, null=True, blank=True)
    place_of_birth = models.CharField(max_length=150, null=True, blank=True)
    ns = (('NIGERIAN', 'NIGERIAN'), ('NON-CITIZEN', 'NON-CITIZEN'))
    nationality = models.CharField(choices=ns,null=True, blank=True, max_length=300)

    zone = models.ForeignKey(Zone, blank=True, null=True,on_delete=models.CASCADE)
    state = models.ForeignKey(State, blank=True,null=True, on_delete=models.CASCADE)
    lga = models.ForeignKey(LGA, blank=True, null=True, on_delete=models.CASCADE)
    senate_district = models.ForeignKey(SenateDistrict, null=True, blank=True, on_delete=models.CASCADE)

    res_add = models.CharField('residential address', max_length=300, null=True, blank=True)
    per_res_addr = models.CharField('permanent residential address', max_length=300, null=True, blank=True)
    spouse = models.CharField(max_length=300, null=True, blank=True)
    hobbies = models.CharField(max_length=300, null=True, blank=True)

    faith = (('ISLAM', 'ISLAM'), ('CHRISTIANITY', 'CHRISTIANITY'),('TRADITIONAL', 'TRADITIONAL'))
    religion = models.CharField(choices=faith, max_length=100, null=True, blank=True)
    qual = models.CharField(max_length=150, null=True, blank=True)

    nofc = models.PositiveIntegerField('number of children', null=True, blank=True)
    nameoc = models.TextField('name of children', max_length=400, null=True, blank=True)
    doboc = models.TextField('date of birth of children',max_length=300, null=True, blank=True)

    fnok_name = models.CharField('first next of kin name', max_length=300, null=True, blank=True)
    fnok_phone = models.PositiveIntegerField('first next of kin phone', null=True, blank=True)
    fnok_email = models.EmailField('first next of kin email', max_length=300, null=True, blank=True)
    fnok_addr = models.CharField('first next of kin address', max_length=300, null=True, blank=True)
    fnok_rel = models.CharField('relationship with first next of kin', max_length=300, null=True, blank=True)
    fnok_photo = models.ImageField('first next of kin photo', null=True, blank=True)

    snok_name = models.CharField('second next of kin name', max_length=300, null=True, blank=True)
    snok_phone = models.PositiveIntegerField('second next of kin phone', null=True, blank=True)
    snok_email = models.EmailField('second next of kin email', max_length=300, null=True, blank=True)
    snok_addr = models.CharField('second next of address', max_length=300, null=True, blank=True)
    snok_rel = models.CharField('second next of kin', max_length=300, null=True, blank=True)
    snok_photo = models.ImageField('second next of kin photo', null=True, blank=True)

    created = models.DateTimeField('date added', auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.created:
            self.created = timezone.now()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('profile_details', args=[self.user])

    def full_name(self):
        parts = [
            self.user.get_full_name() or ' ',
            self.middle_name or ' ',
            str(self.file_no) if self.file_no is not None else ' '
        ]
        return ' '.join(part for part in parts if part.strip()).strip()

    def __str__(self):
        if self.user:
            return f"{self.user.username} {self.user.last_name} {self.user.first_name}"

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
    user = models.ForeignKey(
        User, null=True, on_delete=models.CASCADE, related_name='qual')
    school = models.CharField(max_length=300, null=True, blank=True)
    types = (('PRIMARY', 'PRIMARY'), ('SECONDARY', 'SECONDARY'), ('COLLEGE OF EDUCATION', 'COLLEGE OF EDUCATION'),
             ('POLYTECHNIC', 'POLYTECHNIC'), ('UNIVERSITY', 'UNIVERSITY'))
    school_category = models.CharField(
        choices=types, max_length=300, null=True, blank=True)
    qual = models.CharField(
        'qualification', max_length=300, null=True, blank=True)
    date_obtained = models.DateField(null=True, blank=True)
    created = models.DateTimeField('date added', auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('qual_details', args=[self.user])

    def __str__(self):
        return f"{self.user.last_name} {self.user.first_name}" if self.user else ""


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
        return f"{self.user.last_name} {self.user.first_name} {self.qual_obtained}" if self.user else ""


class GovernmentAppointment(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE,related_name='govapp')
    department = models.ForeignKey(Department,blank=True, max_length=300, null=True,on_delete=models.CASCADE)
    cpost = models.ForeignKey(Post,blank=True, max_length=300, null=True,on_delete=models.CASCADE)
    salary_scale = models.ForeignKey(SalaryScale,blank=True, max_length=300, null=True,on_delete=models.CASCADE)
    grade_level = models.ForeignKey(GradeLevel,blank=True, max_length=300, null=True,on_delete=models.CASCADE)
    type_of_cadre = models.ForeignKey(TypeOfCadre,blank=True, max_length=300, null=True,on_delete=models.CASCADE)
    ippis_no = models.DecimalField('IPPIS number', max_digits=6, decimal_places=0, null=True, unique=True, blank=True)
    date_fapt = models.DateField('date of first appointment', null=True, blank=True)
    date_capt = models.DateField('date of current appointment', null=True, blank=True)
    sfapt = models.FloatField('salary per annum at date of first appointment', null=True, max_length=300, blank=True)  
    step = models.IntegerField(null=True, blank=True)
    ex_status=(('PASS','PASS'),('FAILED','FAILED'))
    exams_status = models.CharField(null=True, blank=True, max_length=100, choices=ex_status)
    due = models.BooleanField(default=False)
    retired = models.BooleanField(default=False)
    cleared = models.BooleanField(default=False)
    rtb=(('DATE OF BIRTH','DATE OF BIRTH'),('DATE OF FIRST APPOINTMENT','DATE OF FIRST APPOINTMENT'))
    retire_by = models.CharField(null=True, blank=True, max_length=100, choices=rtb)
    created = models.DateTimeField('date added', auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.step is not None:
            self.step = min(self.step, 15)  # Assuming maximum step is 15
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('govapp_details', args=[self.user])

    def full_name(self):
        return f"{self.user.get_full_name()}, {self.cpost}"

    def __str__(self):
        return f"{self.user.last_name} {self.user.first_name}" if self.user else ""


class Promotion(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='promotion')
    department = models.ForeignKey(Department,blank=True, max_length=300, null=True,on_delete=models.CASCADE)
    cpost = models.ForeignKey(Post,blank=True, max_length=300, null=True,on_delete=models.CASCADE)
    govapp = models.ForeignKey(GovernmentAppointment, on_delete=models.CASCADE, related_name='progovapp', null=True)
    prom_date = models.DateField('promotion date', null=True, blank=True)
    gl = models.PositiveIntegerField('grade level', null=True, blank=True)
    step = models.PositiveIntegerField(null=True, blank=True)
    inc_date = models.DateField('increment date', null=True, blank=True)
    conf_date = models.DateField('confirmation date', null=True, blank=True)
    created = models.DateTimeField('date added', auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('prom_details', args=[self.user])

    def __str__(self):
        return f"{self.user.last_name} {self.user.first_name}" if self.user else ""


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
        verbose_name_plural = 'Disciplinaries record'

    def __str__(self):
        return f"{self.user.last_name} {self.user.first_name}" if self.user else ""



class Leave(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='leave', null=True)
    nature_of_leave = models.ForeignKey(LeaveTypes, on_delete=models.CASCADE, null=True)
    year = models.PositiveIntegerField(default=timezone.now().year)
    start_date = models.DateField(null=True)
    total_days = models.PositiveIntegerField(blank=True, null=True)
    balance = models.PositiveIntegerField(blank=True, null=True)
    granted_days = models.PositiveIntegerField('number of days granted', null=True)
    status = models.CharField(max_length=300, blank=True, null=True)
    is_leave_over = models.BooleanField(default=False)
    comment = models.TextField('comments if any', blank=True, null=True)
    created = models.DateTimeField('date added', auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('profile_details', kwargs={'username': self.user.username})

    def __str__(self):
        return f"{self.user.last_name} {self.user.first_name}" if self.user else ""

    def clean(self):
        super().clean()
        
        if self.start_date and self.start_date < timezone.now().date():
            raise ValidationError({'start_date': 'Start date cannot be in the past.'})

        if self.nature_of_leave.name.upper() == 'Annual':
            annual_leaves = Leave.objects.filter(
                user=self.user,
                year=self.year,
                nature_of_leave__name__iexact='annual'
            )
            if not self.pk and annual_leaves.count() >= 2:
                raise ValidationError('You cannot take annual leave more than twice a year.')

        if self.granted_days is not None:
            if self.granted_days <= 0:
                raise ValidationError({'granted_days': 'Granted days must be greater than 0.'})
            if self.balance is not None and self.granted_days > self.balance:
                raise ValidationError({'granted_days': 'Granted days cannot exceed the available balance.'})

    def save(self, *args, **kwargs):
        if not self.pk:  # New instance
            last_leave = Leave.objects.filter(
                user=self.user,
                year=self.year,
                nature_of_leave=self.nature_of_leave
            ).order_by('-created').first()

            if last_leave:
                self.balance = last_leave.remain
                self.total_days = last_leave.remain
            else:
                self.balance = self.total_days

        self.full_clean()
        super().save(*args, **kwargs)

    @property
    def remain(self):
        if self.balance is not None and self.granted_days is not None:
            return max(0, self.balance - self.granted_days)
        return None

    @property
    def return_on(self):
        if self.granted_days and self.granted_days > 0:
            return self.start_date + timedelta(days=self.granted_days)
        return None

    @property
    def over(self):
        if self.return_on and self.return_on < timezone.now().date():
            self.is_leave_over = True
            self.save(update_fields=['is_leave_over'])
            return "your leave is over"
        elif self.total_days and self.total_days > 0:
            return "on leave"
        return None

    def clear_leave_over(self):
        if self.is_leave_over:
            self.is_leave_over = False
            self.save(update_fields=['is_leave_over'])

    @property
    def leave_status(self):
        if self.nature_of_leave.name == 'Annual':
            annual_leaves = Leave.objects.filter(
                user=self.user,
                year=self.year,
                nature_of_leave__name__iexact='annual'
            ).count()
            
            if annual_leaves >= 2:
                return "You have already taken the maximum annual leaves for this year."
        
        if self.is_leave_over:
            return "Your leave is over."
        elif self.over == "on leave":
            days_left = (self.return_on - timezone.now().date()).days
            if days_left <= 3:
                return f"Your leave is about to finish in {days_left} day{'s' if days_left > 1 else ''}."
            return f"You are currently on leave. {days_left} days remaining."
        elif self.nature_of_leave.name== 'Annual':
            return f"Your leave balance is {self.remain} days."
        elif not self.nature_of_leave.name== 'Annual':
            return f" "


class ExecutiveAppointment(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='execapp')
    department = models.ForeignKey(Department,blank=True, max_length=300, null=True,on_delete=models.CASCADE)
    cpost = models.ForeignKey(Post,blank=True, max_length=300, null=True,on_delete=models.CASCADE)
    govapp = models.ForeignKey(GovernmentAppointment, on_delete=models.CASCADE, related_name='execgovapp', null=True)
    date = models.DateField(null=True, blank=True)
    status = models.CharField(null=True, max_length=300, blank=True)
    created = models.DateTimeField('date added', auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('exeapp_details', args=[self.user])

    def __str__(self):
        return f"{self.user.last_name} {self.user.first_name}" if self.user else ""



class Retirement(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    date = models.DateField(null=True, blank=True)
    status = models.CharField(null=True, max_length=300, blank=True)
    retire = models.BooleanField(default=False)
    created = models.DateTimeField('date added', auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('rt_details', args=[self.user])

    def __str__(self):
        return f"{self.user.last_name} {self.user.first_name}" if self.user else ""