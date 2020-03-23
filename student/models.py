from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse

# Create your models here.

class User(AbstractUser):
    username           = models.CharField(max_length=256, blank=False, unique=True, default='')
    first_name         = models.CharField(max_length=256, blank=False, default='')
    last_name          = models.CharField(max_length=256, blank=False, default='')
    email              = models.EmailField(unique=True, default='')
    birth_date         = models.DateField(null=True)
    address            = models.TextField(verbose_name='Address', blank=False, default='')
    contact            = models.CharField(max_length=13,blank=False, unique=True, default='')
    roll               = models.CharField(verbose_name='Roll no.',max_length=8, unique=True, blank=False, default='')
    reg                = models.CharField(verbose_name='Registration no.', max_length=8, blank=False, unique=False, default='')
    department         = models.CharField(max_length=256, blank=False, default='')
    year_of_study      = models.CharField(max_length=256, blank=False, default='')
    photograph         = models.ImageField(upload_to='student/images', default='')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'username',
    ]

    def __str__(self):
        full_name = self.first_name + ' ' + self.last_name
        return full_name

    def get_absolute_url(self):
        return reverse('student_profile', kwargs={'pk': self.pk})
