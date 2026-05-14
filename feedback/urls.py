from django.urls import path
from . import views

app_name = 'feedback'

urlpatterns = [
    path('submit/', views.submit_feedback, name='submit_feedback'),
    path('my-feedbacks/', views.my_feedbacks, name='my_feedbacks'),
    path('view/', views.view_feedback, name='view_feedback'),
    path('all/', views.all_feedbacks, name='all_feedbacks'),
    path('<int:feedback_id>/delete/', views.delete_feedback, name='delete_feedback'),
    path('courses/', views.manage_courses, name='manage_courses'),
    path('courses/create/', views.create_course, name='create_course'),
    path('courses/<int:course_id>/edit/', views.edit_course, name='edit_course'),
    path('courses/<int:course_id>/delete/', views.delete_course, name='delete_course'),
    path('export-csv/', views.export_feedback_csv, name='export_csv'),
]
