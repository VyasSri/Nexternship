from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class StudentInfo(models.Model):
    student_name = models.CharField(max_length=100)
    student_grade = models.IntegerField()
    student_email = models.EmailField(max_length=100)
    student_skills = models.CharField(max_length=200)
    student_experience = models.CharField(max_length=200)
    student_info = models.CharField(max_length=200)


class JobPosting(models.Model):
    job_title = models.CharField(max_length=100)
    job_hours = models.IntegerField()
    job_skills = models.CharField(max_length=200)
    job_description = models.CharField(max_length=300)
    company = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

