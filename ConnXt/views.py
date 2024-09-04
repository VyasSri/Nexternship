from django.shortcuts import render
from .forms import StudentForm, JobForm
from .models import JobPosting


# Create your views here.
def home(request):
    return render(request, 'index.html')


def talent(request):
    return render(request, 'talent.html')


def profile(response):
    if response.method == "POST":
        success_msg = None
        error_msg = None
        form = StudentForm(response.POST,)
        if form.is_valid():
            form.save()
            success_msg = "Profile Saved Successfully"
            return render(response, 'profile.html', {'form': form, 'success_msg': success_msg})
        else:
            error_msg = 'Form is invalid. Please correct the errors.'
            return render(response, "profile.html", {"form": form, "error_msg": error_msg})
    else:
        form = StudentForm()
    return render(response, "profile.html", {"form": form})


def employer(response):
    success_msg = None
    error_msg = None
    if response.method == 'POST':
        form = JobForm(response.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.published_by = response.user
            form.save()
            success_msg = "Job Posted Successfully"
            return render(response, 'employerhome.html', {'form': form, "success_msg": success_msg})
        else:
            error_msg = "Form is invalid. Please correct the errors below."
            return render(response, 'employerhome.html', {'form': form, "error_msg": error_msg})
    else:
        form = JobForm()
    return render(response, 'employerhome.html', {'form': form})


def jobs(request):
    job_postings = JobPosting.objects.all()
    return render(request, 'employers.html', {'job_postings': job_postings})


def studentdash(request):
    return render(request, 'studentdashboard.html')


def aboutus(request):
    return render(request, 'aboutus.html')


def studenterror(request):
    return render(request, 'studenterror.html')


def employererror(request):
    return render(request, 'employererror.html')
