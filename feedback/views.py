from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg, Count
from django.http import HttpResponse
import csv

from .models import Feedback, Course
from .forms import FeedbackForm, CourseForm
from accounts.decorators import student_required, lecturer_required, admin_required


@login_required
@student_required
def submit_feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.student = request.user
            feedback.lecturer = feedback.course.lecturer
            feedback.save()
            messages.success(request, 'Feedback submitted successfully!')
            return redirect('accounts:dashboard')
    else:
        form = FeedbackForm()
    return render(request, 'feedback/submit_feedback.html', {'form': form})


@login_required
@student_required
def my_feedbacks(request):
    feedbacks = Feedback.objects.filter(student=request.user).select_related('course', 'lecturer')
    return render(request, 'feedback/my_feedbacks.html', {'feedbacks': feedbacks})


@login_required
@lecturer_required
def view_feedback(request):
    feedbacks = Feedback.objects.filter(lecturer=request.user).select_related('course', 'student')
    course_stats = Course.objects.filter(lecturer=request.user).annotate(
        avg_rating=Avg('feedbacks__rating'),
        feedback_count=Count('feedbacks')
    )
    return render(request, 'feedback/view_feedback.html', {
        'feedbacks': feedbacks,
        'course_stats': course_stats,
    })


@login_required
@admin_required
def all_feedbacks(request):
    feedbacks = Feedback.objects.select_related('student', 'lecturer', 'course').all()
    return render(request, 'feedback/all_feedbacks.html', {'feedbacks': feedbacks})


@login_required
@admin_required
def delete_feedback(request, feedback_id):
    fb = get_object_or_404(Feedback, pk=feedback_id)
    if request.method == 'POST':
        fb.delete()
        messages.success(request, 'Feedback deleted.')
        return redirect('feedback:all_feedbacks')
    return render(request, 'feedback/delete_feedback.html', {'feedback': fb})


@login_required
@admin_required
def manage_courses(request):
    courses = Course.objects.select_related('lecturer').all()
    return render(request, 'feedback/manage_courses.html', {'courses': courses})


@login_required
@admin_required
def create_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Course created successfully.')
            return redirect('feedback:manage_courses')
    else:
        form = CourseForm()
    return render(request, 'feedback/create_course.html', {'form': form})


@login_required
@admin_required
def edit_course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, 'Course updated.')
            return redirect('feedback:manage_courses')
    else:
        form = CourseForm(instance=course)
    return render(request, 'feedback/edit_course.html', {'form': form, 'course': course})


@login_required
@admin_required
def delete_course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    if request.method == 'POST':
        course.delete()
        messages.success(request, 'Course deleted.')
        return redirect('feedback:manage_courses')
    return render(request, 'feedback/delete_course.html', {'course': course})


@login_required
@admin_required
def export_feedback_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="feedback_report.csv"'

    writer = csv.writer(response)
    # Header — 8 columns
    writer.writerow(['Student', 'Anonymous', 'Lecturer', 'Course', 'Rating', 'Comment', 'Suggestions', 'Date'])

    for fb in Feedback.objects.select_related('student', 'lecturer', 'course').all():
        writer.writerow([
            fb.student.get_full_name(),
            'Yes' if fb.is_anonymous else 'No',   # BUG FIX: was missing from original
            fb.lecturer.get_full_name(),
            fb.course.name,
            fb.rating,
            fb.comment,
            fb.suggestions,
            fb.created_at.strftime('%Y-%m-%d %H:%M'),
        ])

    return response
