from django.contrib.auth.decorators import login_required

from .forms import StudentForm, JobForm
from .models import JobPosting, StudentInfo, JobApplication
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect




# Create your views here.
def home(request):
    return render(request, 'index.html')

def talent(request):
    message = ""
    
    if request.method == 'POST' and 'application_id' in request.POST:
        application_id = request.POST.get('application_id')
        action = request.POST.get('action')
        application = get_object_or_404(JobApplication, id=application_id)
        
        # Accept or Reject the application
        if action == 'accept':
            application.accepted = True
            message = f"{application.student.student_name} has been accepted."
        elif action == 'reject':
            application.rejected = True
            message = f"{application.student.student_name} has been rejected."
        
        application.save()
        
        # Redirect to the same page with a message to prevent form resubmission
        return redirect('talent')

    # Only show applications that are still pending (not accepted or rejected)
    job_applications = JobApplication.objects.filter(accepted=False, rejected=False)
    
    return render(request, 'talent.html', {
        'job_applications': job_applications,
        'message': message,
    })


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

    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            # Save the job posting
            job = form.save(commit=False)
            job.user = request.user  # Attach the current logged-in user as the job poster
            job.save()
            success_msg = "Job Posted Successfully"
            form = JobForm()  # Reset the form after successful submission
        else:
            # If form is invalid, show the error message
            error_msg = "Form is invalid. Please correct the errors below."
    else:
        # If it's not a POST request, show a blank form
        form = JobForm()

    # Render the page with success or error messages
    return render(request, 'employerhome.html', {'form': form, 'success_msg': success_msg, 'error_msg': error_msg})

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

@login_required
def employer_list(request):
    # Fetch all job applications where 'accepted' is True
    accepted_applications = JobApplication.objects.filter(accepted=True)

    # Pass the accepted applications to the template
    return render(request, 'employer_list.html', {'accepted_applications': accepted_applications})