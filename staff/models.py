from django.db import models
from django.contrib.auth.models import User
from django.core.validators import  MaxValueValidator
from django.core.exceptions import ValidationError
from datetime import timedelta, date
from django.db import models 
from django.urls import reverse
from django.contrib import messages



def valMax(v):
    mdigits=4
    vstr=str(v)
    if len(vstr)>mdigits:
        raise ValidationError(f'Maximum {mdigits} digits allowed')
    
class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    email=models.EmailField(blank=True, null=True, max_length=100, unique=True)
    photo = models.ImageField(null=True)
    file_no = models.PositiveIntegerField('file number', null=True, unique=True, blank=False, validators=[valMax, MaxValueValidator(999999)])
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
    geo_political_zone=(('NORTH-EAST','NORTH-EAST'),('NORTH-WEST','NORTH-WEST'),('NORTH-CENTRAL','NORTH-CENTRAL'),('SOUTH-EAST','SOUTH-EAST'),('SOUTH-WEST','SOUTH-WEST'),('SOUTH-SOUTH','SOUTH-SOUTH')) 
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
    fnok_no = models.PositiveIntegerField('first next of kin phone',null=True, blank=True)
    fnok_email = models.EmailField('first next of kin email',max_length=300, null=True, blank=True)
    fnok_addr = models.CharField('first next of kin address',max_length=300, null=True, blank=True)
    fnok_rel = models.CharField('relationship with first next of kin', max_length=300, null=True, blank=True)
    fnok_photo = models.ImageField(null=True)
    snok_name = models.CharField('second next of kin name', max_length=300, null=True, blank=True)
    snok_phone = models.PositiveIntegerField('second next of kin phone', null=True, blank=True)
    snok_email = models.EmailField('second next of kin email', max_length=300, null=True, blank=True)
    snok_addr = models.CharField('second next of address', max_length=300, null=True, blank=True)
    snok_rel = models.CharField('second next of kin', max_length=300, null=True, blank=True)
    snok_photo = models.ImageField(null=True)
    timestamp = models.DateTimeField('date added', auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('profile_details', args=[self.user])

    def __str__(self):
        if self.user:
            return f"{self.user.first_name} {self.user.last_name}"

    def age(self):
        today=date.today()
        if self.dob:
            age=today.year-self.dob.year

            if today.month<self.dob.month or (today.month==self.dob.month and today.day < self.dob.day):
                age-=1        
            return age
    
    def dob(self):
        today=date.today()
        if self.dob is not None:
            is_dob=today.month==self.dob.month and today.day ==self.dob.day
            if is_dob:
                return is_dob


class Qualification(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='qual')
    school = models.CharField(max_length=300,null=True, blank=True)
    types=(('PRIMARY','PRIMARY'),('SECONDARY','SECONDARY'), ('COLLEGE OF EDUCATION','COLLEGE OF EDUCATION'),('POLYTECHNIC','POLYTECHNIC')('UNIVERSITY','UNIVERSITY'))
    school_category=models.CharField(choices=types, max_length=300, null=True, blank=True)
    qual = models.CharField('qualification',max_length=300,null=True,blank=True)    
    date_obtained = models.DateField(null=True,blank=True)
    timestamp = models.DateTimeField('date added', auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('qual_details', args=[self.user])

    def __str__(self):
        if self.user:
            return f"{self.user.first_name} {self.user.last_name}"


class ProfessionalQualification(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='pro_qual')
    institute = models.CharField(max_length=300,null=True,blank=True)
    inst_address = models.CharField('institute address', null=True,max_length=300,blank=True)
    qual_obtained = models.CharField('qualification obtained',null=True,max_length=300,blank=True)
    date_obtained = models.DateField(null=True,blank=True)
    timestamp = models.DateTimeField('date added',auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
   
    def get_absolute_url(self):
        return reverse('pro_qual_details', args=[self.user])

    def __str__(self):
        if self.user:
            return f"{self.user.first_name} {self.user.last_name}"

def vMax(v):
    mdigits=6
    vstr=str(v)
    if len(vstr)>mdigits:
        raise ValidationError(f'Maximum {mdigits} digits allowed')

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
    ippis_no = models.PositiveIntegerField('IPPIS number', null=True, unique=True, blank=True,validators=[vMax,MaxValueValidator(999999)])
    date_fapt = models.DateField('date of first appointment', null=True,blank=True)
    date_capt = models.DateField('date of current appointment', null=True,blank=True)
    tp=(('CASUAL','CASUAL'),('LOCUM','LOCUM'),('PERMANENT','PERMANENT'),('PROBATION', 'PROBATION'))
    type_of_appt=models.CharField('type of appointment', choices=tp, null=True,max_length=300,blank=True)
    sfapt = models.FloatField('salary_per_annum_at_date_of_first_appointment', null=True,max_length=300,blank=True)    
    ss=(('CONHESS','CONHESS'),('CONMESS','CONMESS'), ('GIPMIS','GIPMIS'))
    salary_scale = models.CharField(choices=ss, null=True,max_length=300,blank=True)    
    gl=(('03','03'),('04','04'),('05','05'),('06','06'),('07','07'),('08','08'),('09','09'),('11','11'),('12','12'),('13','13'),('14','14'),('15','15'))
    grade_level = models.CharField(choices=gl, null=True,max_length=300,blank=True)
    step = models.PositiveIntegerField(null=True, blank=True)
    tc=(('JUNIOR','JUNIOR'), ('SENIOR','SENIOR'),('EXECUTIVE','EXECUTIVE'))
    type_of_cadre=models.CharField(choices=tc, null=True, blank=True, max_length=100)
    exams_status = models.CharField(null=True, blank=True, max_length=100)
    retire=models.BooleanField(null=True, blank=True)
    rtb=models.CharField('retired by', null=True, blank=True,max_length=50)
    due=models.BooleanField('due for promotion', null=True, blank=True)
    timestamp = models.DateTimeField('date added', auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('govapp_details', args=[self.user])

    def __str__(self):
        if self.user:
            return f"{self.user.first_name} {self.user.last_name}"

    #step calculation
    def step_inc(self):
        today=date.today()
        if self.step is not None:
            if today.month == 1 and today.day == 1:
                self.step +=1
         

class Promotion(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='promotion')
    cpost = models.CharField('current post',null=True,max_length=300,blank=True)
    govapp=models.ForeignKey(GovernmentAppointment, on_delete=models.CASCADE, related_name='govapp')
    prom_date = models.DateField('promotion date',null=True,blank=True)
    gl = models.PositiveIntegerField('grade level',null=True,blank=True)
    step = models.PositiveIntegerField(null=True,blank=True)
    inc_date = models.DateField('increment date', null=True,blank=True)
    conf_date = models.DateField('confirmation date', null=True,blank=True)
    timestamp = models.DateTimeField('date added', auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('prom_details', args=[self.user])

    def __str__(self):
        if self.user:
            return f"{self.user.last_name} {self.user.first_name}"

    #promotion calculation
    def prom_cal(self,request):
        today=date.today()

        if self.govapp.date_capt is not None:
            cal=self.govapp.date_capt.year
            ex=self.govapp.exams_status
            gl=self.govapp.grade_level
            tc=self.govapp.type_of_cadre
            
            #performing checks
            if cal is not None:
                if today.year-cal  == 3 and int(gl) >= 6 and ex == 'pass' and tc == 'SENIOR':
                    self.govapp.due = True  
                    self.govapp.save()
                    return messages.success(request,'DUE FOR PROMOTION')
                elif today.year-cal  == 2 and int(gl) <= 5 and ex == 'pass' and tc == 'JUNIOR':
                    self.govapp.due = True    
                    self.govapp.save()
                    return messages.success(request,'DUE FOR PROMOTION')
                elif today.year-cal  == 4 and int(gl) >= 13 and ex == 'pass' and tc == 'EXECUTIVE':
                    self.govapp.due = True    
                    self.govapp.save()
                    return messages.success(request,'DUE FOR PROMOTION')
                else:
                    self.govapp.due = False
                    self.govapp.save()


class Discipline(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='discipline')
    offense = models.TextField(null=True,blank=True)
    decision = models.TextField(null=True,blank=True)
    date = models.DateField(null=True,blank=True)
    comment = models.TextField(null=True,blank=True)
    timestamp = models.DateTimeField('date added', auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('dis_details', args=[self.user])

    class Meta:
        verbose_name_plural='Disciplinaries'
    
    def __str__(self):
        if self.user:
            return f"{self.user.last_name} {self.user.first_name}"


class Leave(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='leave')
    nature = models.CharField('nature of leave', null=True,max_length=300,blank=True)
    year = models.PositiveIntegerField(null=True,blank=True)
    start_date = models.DateField(null=True,blank=False)
    total_days=models.PositiveIntegerField(null=True, blank=True)
    balance=models.PositiveIntegerField(null=True,blank=True)
    granted = models.PositiveIntegerField('number of days granted',null=True, blank=False)
    status = models.CharField(null=True,max_length=300,blank=True)
    lv=models.BooleanField(blank=True, null=True)
    comments = models.TextField('comments if any', null=True,blank=True)
    timestamp = models.DateTimeField('date added', auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('lv_details', args=[self.user])
 
    def __str__(self):
        if self.user:
            return f"{self.user.last_name} {self.user.first_name}"

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
    
    def remain(self):
        if self.total_days is not None and self.granted is not None:
            return self.total_days - self.granted

    def clean(self):
        super().clean()

        r = self.remain()
        if r <= 0 or self.granted == 0:
            raise ValidationError('Invalid entry. Please try again.')
        
    @property    
    def return_on(self):
        if self.granted is not None:
            if self.granted > 0:
                ddays=self.total_days-self.remain()
                timedelta_o=timedelta(days=ddays)
                new_date=self.start_date+timedelta_o
                if new_date is not None:
                    return new_date
    
    def over(self):        
        today=date.today()
        if self.remain() is not None and self.remain() <= 0 and today == self.return_on:
            self.lv = True
        else:
            self.lv = False
        self.lv.save()

class ExecutiveAppointment(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='execapp')
    designation = models.CharField(null=True,max_length=300,blank=True)
    date = models.DateField(null=True,blank=True)
    status = models.CharField(null=True,max_length=300,blank=True)
    timestamp = models.DateTimeField('date added', auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('exeapp_details', args=[self.user])
    
    def __str__(self):
        if self.user:
            return f"{self.user.last_name} {self.user.first_name}"


class Retirement(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    date = models.DateField(null=True,blank=True)
    govapp=models.ForeignKey(GovernmentAppointment, on_delete=models.CASCADE, related_name='govapp')
    profile=models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='profile')
    status = models.CharField(null=True,max_length=300,blank=True)
    timestamp = models.DateTimeField('date added', auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('rt_details', args=[self.user])
    
    def __str__(self):
        if self.user:
            return f"{self.user.last_name} {self.user.first_name}"
    
    def rt(self):
        today=date.today()
        art=self.profile.age()
        drt=self.govapp.date_fapt

        if drt is not None:
            drt=today.year-drt.year

        if art is not None and art >= 65:
            self.govapp.retire = True
            self.govapp.rtb = "RETIRE BY DATE OF BIRTH"
            self.govapp.save()
        elif drt is not None and drt >= 35:
            self.govapp.retire = True
            self.govapp.rtb = "RETIRE BY DATE OF APPOINTMENT"
            self.govapp.save()
        else:
            self.govapp.retire = False
            self.govapp.save()