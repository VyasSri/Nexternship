from django.contrib.auth.decorators import login_required

from .forms import StudentForm, JobForm
from .models import JobPosting
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect


# Create your views here.
def home(request):
    return render(request, 'index.html')


def talent(request):
    return render(request, 'talent.html')


def profile(response):
    if response.method == "POST":
        success_msg = None
        error_msg = None
        form = StudentForm(response.POST, )
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


def employer(request):
    success_msg = None
    error_msg = None
    form = JobForm()  # Initialize the form at the start

    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.user = request.user  # Assign the user who posted the job
            job.save()
            success_msg = "Job Posted Successfully"
            form = JobForm()  # Reinitialize the form after successful submission
        else:
            error_msg = "Form is invalid. Please correct the errors below."

    return render(request, 'employerhome.html', {'form': form, "success_msg": success_msg, "error_msg": error_msg})


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


def edit_job(request, id):
    job = get_object_or_404(JobPosting, id=id)

    # Ensure the current user is the one who posted the job
    if job.user != request.user:
        return HttpResponseForbidden("You are not allowed to edit this job.")

    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect('/jobedit')  # Replace 'job_list' with your job list view or URL name
    else:
        form = JobForm(instance=job)

    return render(request, 'edit_job.html', {'form': form, 'job': job})


@login_required

@login_required
def delete_job(request, id):
    job = get_object_or_404(JobPosting, id=id)

    # Ensure the current user is the one who posted the job
    if job.user != request.user:
        return HttpResponseForbidden("You are not allowed to delete this job.")

    if request.method == 'POST':
        job.delete()  # Deletes the job from the database
        return redirect('/jobedit')  # Redirect back to the list of jobs

    return render(request, 'confirm_delete.html', {'job': job})

@login_required
def jobedit(request):
    jobs = JobPosting.objects.filter(user=request.user)  # Only show jobs posted by the logged-in user
    return render(request, 'jobedit.html', {'jobs': jobs})