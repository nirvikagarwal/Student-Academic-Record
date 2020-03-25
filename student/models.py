from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse

# Create your models here.

class Department(models.Model):
    name = models.CharField(max_length=100, null=True)
    code = models.CharField(max_length=3, null=True)

    def __str__(self):
        return self.name

class AllSubject(models.Model): #Admin can Enter all the available subjects with their credit points and students can choose from it
    name = models.CharField(max_length=50, null=True)
    code = models.CharField(max_length=10, null=True)
    credit_points = models.IntegerField(null=True)

    def __str__(self):
        return self.name

class AllSemester(models.Model): # student can select their Semesters from this table
    SEMESTER = (
        ('First Semester', 'First Semester'),
        ('Second Semester', 'Second Semester'),
        ('Third Semester', 'Third Semester'),
        ('Fourth Semester', 'Fourth Semester'),
        ('Fifth Semester', 'Fifth Semester'),
        ('Sixth Semester', 'Sixth Semester'),
        ('Seventh Semester', 'Seventh Semester'),
        ('Eighth Semester', 'Eighth Semester'),
    )
    semester = models.CharField(max_length=20, null=True, choices=SEMESTER)

    def __str__(self):
        return self.semester

class User(AbstractUser):

    first_name    = models.CharField(max_length=256,blank=False,null=True)
    last_name     = models.CharField(max_length=256,blank=False,null=True)
    username      = models.CharField(max_length=256,blank=False, unique=True,null=True)
    email         = models.EmailField(unique=True,null=True)
    birth_date    = models.DateField(null=True)
    reg           = models.CharField(verbose_name='Registration no.',max_length=8,blank=False,unique=True,null=True)
    photograph    = models.ImageField(upload_to='student/images',null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'username',
    ]

    def __str__(self):
        return self.email


class StudentSubject(models.Model): # A model which has the subjects of the students semesterwise
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    semester = models.ForeignKey(AllSemester, on_delete=models.CASCADE, null=True)
    subjects = models.ManyToManyField(AllSubject)


# Model which has the marks of all subjects of a student in a semester
class Marks(models.Model):  
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    semester = models.ForeignKey(AllSemester, on_delete=models.CASCADE)
    subject = models.ForeignKey(AllSubject, on_delete=models.CASCADE)
    marks = models.FloatField(null=True)

    def __str__(self):
        return self.student.email

class StudentProfile(models.Model):
    student = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    roll = models.CharField(verbose_name='Roll no.',max_length=8,unique=True,blank=False,null=True)
    address       = models.TextField(verbose_name='Address',blank=False,null=True)
    contact       = models.CharField(max_length=13,blank=False,unique=True,null=True)

    def __str__(self):
        return self.student.email

