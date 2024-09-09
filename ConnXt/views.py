from django.contrib.auth.decorators import login_required

from .forms import StudentForm, JobForm
from .models import JobPosting, StudentInfo, JobApplication
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect




# Create your views here.
def home(request):
    return render(request, 'index.html')


def talent(request):
    if request.method == 'POST' and 'application_id' in request.POST:
        application_id = request.POST.get('application_id')
        try:
            # Attempt to retrieve and delete the job application
            application = get_object_or_404(JobApplication, id=application_id)
            application.delete()  # Delete the application from the database
            return redirect('talent')  # Reload the talent pool page after deletion
        except JobApplication.DoesNotExist:
            # If for some reason the application wasn't found, return an error
            return render(request, 'talent.html', {
                'job_applications': JobApplication.objects.all(),
                'message': 'Application not found or already deleted.'
            })

        # For GET requests, display the current job applications
    job_applications = JobApplication.objects.all()
    return render(request, 'talent.html', {'job_applications': job_applications})

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
    job_postings = JobPosting.objects.all()  # Get all job postings
    message = None  # Initialize message

    # Get student info related to the logged-in user (assuming 1-to-1 relationship with User)
    student_info = StudentInfo.objects.filter(student_email=request.user.email).first()

    # Check if the user is applying for a job
    if request.method == 'POST' and 'apply_job_id' in request.POST:
        job_id = request.POST.get('apply_job_id')
        job = get_object_or_404(JobPosting, id=job_id)

        # Check if the student has filled in their profile
        if student_info and student_info.student_skills and student_info.student_experience:
            # Save the job application
            JobApplication.objects.create(job=job, student=student_info)
            message = "Application Successful"
        else:
            # If profile is incomplete, display an error message
            message = "Application Unsuccessful, Double Check your Profile"

    return render(request, 'employers.html', {'job_postings': job_postings, 'message': message})

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