from django.shortcuts import redirect
from functools import wraps

def role_required(role):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('accounts:login')
            if request.user.role != role:
                return redirect('accounts:dashboard')
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator

def student_required(view_func):
    return role_required('student')(view_func)

def lecturer_required(view_func):
    return role_required('lecturer')(view_func)

def admin_required(view_func):
    return role_required('admin')(view_func)
