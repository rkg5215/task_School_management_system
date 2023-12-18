from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models



class Class(models.Model):
    class_name = models.CharField(max_length=50)
    class_details = models.CharField(max_length=200)

    def __str__(self):
        return self.class_name


class Student(models.Model):
    STATUS_CHOICES = [
        ('inactive', 'Inactive'),
        ('active', 'Active'),

    ]
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    password = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='inactive')
    image = models.ImageField(upload_to='student_images/')
    student_class = models.ForeignKey(Class, on_delete=models.CASCADE)

    def __str__(self):
        return self.first_name