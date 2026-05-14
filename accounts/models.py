from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('lecturer', 'Lecturer'),
        ('admin', 'Administrator'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    student_id = models.CharField(max_length=20, blank=True, null=True, unique=True)
    department = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=15, blank=True)

    def is_student(self):
        return self.role == 'student'

    def is_lecturer(self):
        return self.role == 'lecturer'

    def is_admin_user(self):
        return self.role == 'admin'

    def __str__(self):
        return f"{self.get_full_name()} ({self.role})"
