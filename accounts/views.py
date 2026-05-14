from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg
from .forms import StudentRegistrationForm, LoginForm, UserEditForm, LecturerCreationForm
from .models import User
from .decorators import admin_required
from feedback.models import Feedback, Course

def register_view(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful! Welcome.')
            return redirect('accounts:dashboard')
    else:
        form = StudentRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name}!')
            return redirect('accounts:dashboard')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})
    

def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('accounts:login')

@login_required
def dashboard_view(request):
    user = request.user
    
    # 🔥 FIRST check Django superuser
    if user.is_superuser:
        return redirect('/admin/')  # Django admin panel

    if user.role == 'student':
        feedbacks = Feedback.objects.filter(student=user).select_related('course', 'lecturer')
        courses = Course.objects.all()
        return render(request, 'accounts/student_dashboard.html', {
            'feedbacks': feedbacks,
            'courses': courses,
        })
    elif user.role == 'lecturer':
        feedbacks = Feedback.objects.filter(lecturer=user).select_related('course', 'student')
        avg_rating = feedbacks.aggregate(avg=Avg('rating'))['avg'] or 0
        total = feedbacks.count()
        courses = Course.objects.filter(lecturer=user)
        return render(request, 'accounts/lecturer_dashboard.html', {
            'feedbacks': feedbacks,
            'avg_rating': round(avg_rating, 1),
            'total_feedbacks': total,
            'courses': courses,
        })
    elif user.role == 'admin':
        total_students = User.objects.filter(role='student').count()
        total_lecturers = User.objects.filter(role='lecturer').count()
        total_feedbacks = Feedback.objects.count()
        total_courses = Course.objects.count()
        recent_feedbacks = Feedback.objects.select_related('student', 'lecturer', 'course').order_by('-created_at')[:10]
        return render(request, 'accounts/admin_dashboard.html', {
            'total_students': total_students,
            'total_lecturers': total_lecturers,
            'total_feedbacks': total_feedbacks,
            'total_courses': total_courses,
            'recent_feedbacks': recent_feedbacks,
        })
    if user.is_superuser:
        return redirect('/admin/')
    return redirect('accounts:login')

@login_required
@admin_required
def manage_users(request):
    users = User.objects.all().order_by('role', 'last_name')
    return render(request, 'accounts/manage_users.html', {'users': users})

@login_required
@admin_required
def edit_user(request, user_id):
    user_obj = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user_obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'User updated successfully.')
            return redirect('accounts:manage_users')
    else:
        form = UserEditForm(instance=user_obj)
    return render(request, 'accounts/edit_user.html', {'form': form, 'user_obj': user_obj})

@login_required
@admin_required
def delete_user(request, user_id):
    user_obj = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        user_obj.delete()
        messages.success(request, 'User deleted successfully.')
        return redirect('accounts:manage_users')
    return render(request, 'accounts/delete_user.html', {'user_obj': user_obj})

@login_required
@admin_required
def create_lecturer(request):
    if request.method == 'POST':
        form = LecturerCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Lecturer account created successfully.')
            return redirect('accounts:manage_users')
    else:
        form = LecturerCreationForm()
    return render(request, 'accounts/create_lecturer.html', {'form': form})
