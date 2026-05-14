from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

class Course(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True)
    lecturer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='courses', limit_choices_to={'role': 'lecturer'})
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.code} - {self.name}"

# class Faculty(models.Model):
#     name = models.CharField(max_length=100)

#     def _str_(self):
#         return self.name

class Feedback(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='submitted_feedbacks', limit_choices_to={'role': 'student'})
    lecturer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_feedbacks', limit_choices_to={'role': 'lecturer'})
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='feedbacks')
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    suggestions = models.TextField(blank=True)
    is_anonymous = models.BooleanField(default=False, help_text='If checked, your name will be hidden from the lecturer.')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['student', 'course']

    def __str__(self):
        name = "Anonymous" if self.is_anonymous else str(self.student)
        return f"Feedback by {name} for {self.course} ({self.rating}/5)"

    def get_display_name(self):
        """Returns student name or 'Anonymous Student' based on is_anonymous flag."""
        if self.is_anonymous:
            return "Anonymous Student"
        return self.student.get_full_name() or self.student.username