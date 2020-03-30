from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
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


class StudentSubject(models.Model): # A model which has the subjects of the students semesterwise
    student = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    semester = models.ForeignKey(AllSemester, on_delete=models.CASCADE, null=True)
    subjects = models.ManyToManyField(AllSubject)

    def __str__(self):
        return (self.student.first_name + ' ' + self.semester.semester)


# Model which has the marks of all subjects of a student in a semester
class StudentMarks(models.Model):  
    student = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    semester = models.ForeignKey(AllSemester, on_delete=models.CASCADE, null=True)
    subject = models.ForeignKey(AllSubject, on_delete=models.CASCADE, null=True,)
    marks = models.FloatField(null=True)

    def __str__(self):
        return (self.student.first_name + ' ' + self.semester.semester)



class StudentProfile(models.Model):

    student = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    birth_date    = models.DateField(null=True)
    reg           = models.CharField(verbose_name='Registration no.',max_length=8,blank=False,unique=True,null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True)
    roll = models.CharField(verbose_name='Roll no.',max_length=8,unique=True,blank=False,null=True)
    address       = models.TextField(verbose_name='Address',blank=False,null=True)
    contact       = models.CharField(max_length=13,blank=False,unique=True,null=True)
    photograph    = models.ImageField(upload_to='student/images',null=True, default='student/images/default.png')

    def __str__(self):
        return self.student.username


# USED SIGNALS
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):

    if created:
        StudentProfile.objects.create(student=instance)
        StudentSubject.objects.create(student=instance)
        StudentMarks.objects.create(student=instance)
        print('Profile created')  # Added a print statement for verification