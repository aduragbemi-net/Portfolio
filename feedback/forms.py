from django import forms
from .models import Feedback, Course

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['course', 'rating', 'comment', 'suggestions', 'is_anonymous']
        widgets = {
            'course': forms.Select(attrs={'class': 'form-input'}),
            'rating': forms.HiddenInput(),
            'comment': forms.Textarea(attrs={'class': 'form-input', 'rows': 4, 'placeholder': 'Write your feedback here...'}),
            'suggestions': forms.Textarea(attrs={'class': 'form-input', 'rows': 3, 'placeholder': 'Any suggestions for improvement?'}),
            'is_anonymous': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }
        labels = {
            'is_anonymous': 'Submit anonymously (your name will be hidden from the lecturer)',
        }

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'code', 'description', 'lecturer']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Course Name'}),
            'code': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Course Code'}),
            'description': forms.Textarea(attrs={'class': 'form-input', 'rows': 3, 'placeholder': 'Course Description'}),
            'lecturer': forms.Select(attrs={'class': 'form-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from accounts.models import User
        self.fields['lecturer'].queryset = User.objects.filter(role='lecturer')
