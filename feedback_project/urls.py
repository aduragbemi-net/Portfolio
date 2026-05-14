from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('feedback/', include('feedback.urls')),
    path('', lambda request: redirect('accounts:login')),
]
