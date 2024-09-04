from django.forms import ModelForm
from django import forms
from .models import StudentInfo, JobPosting


class StudentForm(ModelForm):
    class Meta:
        model = StudentInfo
        fields = ['student_name', 'student_grade', 'student_email', 'student_skills', 'student_experience',
                  'student_info']
        widgets = {
            'student_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
            'student_grade': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Grade'}),
            'student_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'student_skills': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Technical Skills'}),
            'student_experience': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Work Experience'}),
            'student_info': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Additional Info'}),
        }


class JobForm(ModelForm):
    class Meta:
        model = JobPosting
        fields = ['job_title', 'job_hours', 'job_skills', 'job_description', 'company']
        widgets = {
            'job_title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Job Title'}),
            'job_hours': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Approximate Hours/Week'}),
            'job_skills': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Skills Required'}),
            'job_description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Job Description'}),
            'company': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Company Name'}),
        }
