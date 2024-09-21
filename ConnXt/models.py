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
    job_description = models.TextField()
    company = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job_date = models.CharField(max_length=100, default='')
    job_location = models.CharField(max_length=100, default='')
    job_capacity = models.IntegerField()

    def __str__(self):
        return self.job_title


class JobApplication(models.Model):
    job = models.ForeignKey(JobPosting, on_delete=models.CASCADE)
    student = models.ForeignKey(StudentInfo, on_delete=models.CASCADE)
    applied_at = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default= False)
    rejected = models.BooleanField(default= False)

    def __str__(self):
        return f'{self.student.student_name} applied to {self.job.job_title}'
