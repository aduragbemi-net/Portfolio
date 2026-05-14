from django.contrib import admin
from .models import Course, Feedback

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'lecturer', 'created_at')
    search_fields = ('name', 'code')

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('student', 'lecturer', 'course', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('comment',)
