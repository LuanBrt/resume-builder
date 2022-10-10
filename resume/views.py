import io
import weasyprint as wp
from django.http import FileResponse, Http404, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.template.loader import render_to_string
from django.contrib.staticfiles import finders
from django.contrib.auth.decorators import login_required
from resume.forms import ResumeCourseForm, ResumeHeaderForm, ResumeJobForm, ResumeSkillForm, ResumeSummaryForm
from resume.models import Resume, ResumeCourse, ResumeJob, ResumeSkill

@login_required
def index_view(request):
    qs = Resume.objects.filter(user=request.user)
    context = {
        'qs': qs
    }
    return render(request, 'resume/index.html', context)

@login_required
def generate_pdf(request, resume_id):
    """ Rendering the resume data in a template """
    
    resume = Resume.objects.get(id=resume_id, user=request.user)
    context = {
        'resume': resume,
    }
    
    buffer = io.BytesIO()
    html_string = render_to_string('pdf/template_1.html', context)
    html = wp.HTML(string=html_string, base_url=request.build_absolute_uri('/'))
    css = wp.CSS(filename=finders.find('template_1_style.css'))
    html.write_pdf(buffer, stylesheets=[css], zoom=1)
    buffer.seek(0)
    return FileResponse(buffer, filename="resume.pdf")

@login_required
def delete_resume_hx_view(request, resume_id):
    if not request.htmx:
        raise Http404
    
    resume = Resume.objects.get(id=resume_id, user=request.user)

    if resume is not None:
        resume.delete()

    return HttpResponse()

@login_required
def create_header_view(request):
    form = ResumeHeaderForm(request.POST or None, request.FILES or None)
    context = {
        'form': form
    }

    if form.is_valid():
        resume_header = form.save()
        Resume.objects.create(resume_header=resume_header, user=request.user)
        return redirect(resume_header.get_edit_url())


    return render(request, 'resume/create-header.html', context)

@login_required
def edit_header_view(request, resume_id):
    resume = Resume.objects.get(id=resume_id, user=request.user)
    form = ResumeHeaderForm(request.POST or None, request.FILES or None, instance=resume.resume_header)
    
    context = {
        'form': form,
        'resume': resume,
    }

    if form.is_valid():
        form.save()
        
    return render(request, 'resume/create-header.html', context)

@login_required
def create_professional_summary_view(request, resume_id):
    form = ResumeSummaryForm(request.POST or None)
    resume = Resume.objects.get(id=resume_id, user=request.user)

    if resume.resume_professional_summary is not None:
        return redirect(resume.resume_professional_summary.get_edit_url())

    context = {
        'form': form,
        'resume': resume,
    }

    if form.is_valid():
        summary = form.save()
        resume.resume_professional_summary = summary
        resume.save()
        return redirect(summary.get_edit_url())

    return render(request, 'resume/create-professional-summary.html', context)

@login_required
def edit_professional_summary_view(request, resume_id):
    if resume_id is None:
        raise Http404

    resume = Resume.objects.get(id=resume_id, user=request.user)
    professional_summary = resume.resume_professional_summary

    form = ResumeSummaryForm(request.POST or None, instance=professional_summary)
    context = {
        'form': form,
        'resume': resume,
    }

    if form.is_valid():
        form_summary = form.save()
        resume.resume_professional_summary = form_summary
        resume.save()
        return redirect(form_summary.get_edit_url())

    return render(request, 'resume/create-professional-summary.html', context)

@login_required
def create_skills_view(request, resume_id):
    return create_object_generic_view(request, resume_id, 'hx-skill-new', 'create-skills.html', 'skill')
@login_required
def create_jobs_view(request, resume_id):
    return create_object_generic_view(request, resume_id, 'hx-job-new', 'create-jobs.html', 'job')
@login_required
def create_courses_view(request, resume_id):
    return create_object_generic_view(request, resume_id, 'hx-course-new', 'create-courses.html', 'course')

@login_required
def create_update_skills_hx_view(request, resume_id, object_id=None):
    success_template = f'resume/partials/skill-form.html'
    return create_update_object_hx_generic_view(request, resume_id, object_id, 'hx-skill-new', ResumeSkill, ResumeSkillForm, 'skill', success_template)
@login_required
def create_update_jobs_hx_view(request, resume_id ,object_id=None):
    success_template = f'resume/partials/job-inline.html'
    return create_update_object_hx_generic_view(request, resume_id, object_id, 'hx-job-new', ResumeJob, ResumeJobForm, 'job', success_template)
@login_required
def create_update_courses_hx_view(request, resume_id, object_id=None):
    success_template = f'resume/partials/course-inline.html'
    return create_update_object_hx_generic_view(request, resume_id, object_id, 'hx-course-new', ResumeCourse, ResumeCourseForm, 'course', success_template)

@login_required
def delete_skill_hx_view(request, resume_id, object_id):
    return delete_object_hx_generic_view(request, resume_id, object_id, ResumeSkill)
@login_required
def delete_job_hx_view(request, resume_id, object_id):
    return delete_object_hx_generic_view(request, resume_id, object_id, ResumeJob)
@login_required
def delete_course_hx_view(request, resume_id, object_id):
    return delete_object_hx_generic_view(request, resume_id, object_id, ResumeCourse)


def create_object_generic_view(request, resume_id, reverse_url, template_name, generic_name):
    # to be used on the add more buttons
    if resume_id is None:
        raise Http404

    resume = Resume.objects.get(id=resume_id, user=request.user)

    new_object_url = reverse(f'resume:{reverse_url}', kwargs={'resume_id': resume.id})

    context = {
        'resume': resume,
        f'new_{generic_name}_url': new_object_url
    }

    return render(request, f'resume/{template_name}', context)

def delete_object_hx_generic_view(request, resume_id, object_id, ResumeObjectClass):
    if not request.htmx:
        raise Http404
    
    resume = Resume.objects.get(id=resume_id, user=request.user)

    object_instance = None
    if object_id is not None:
        object_instance = ResumeObjectClass.objects.get(parent_resume=resume, id=object_id)
        object_instance.delete()

    return HttpResponse()

def create_update_object_hx_generic_view(request, resume_id, object_id, reverse_url, ResumeObjectClass, ResumeObjectClassForm, generic_name, success_template):
    if not request.htmx:
        raise Http404

    resume = Resume.objects.get(id=resume_id, user=request.user)

    object_instance = None
    hx_url = reverse(f'resume:{reverse_url}', kwargs={'resume_id': resume.id}) # url for form hx request
    if object_id is not None:
        object_instance = ResumeObjectClass.objects.get(parent_resume=resume, id=object_id)
        hx_url = object_instance.get_edit_url() # if there is an instance based on the id, the url will be for update

    form = ResumeObjectClassForm(request.POST or None, instance=object_instance)

    context = {
        'form': form,
        generic_name: object_instance,
        'hx_url': hx_url,
        'resume': resume,
    }

    if form.is_valid():
        form_object = form.save(commit=False)
        if object_instance is None:
            form_object.parent_resume = resume
        form_object.save()
        context[generic_name] = form_object
        return render(request, success_template, context)

    return render(request, f'resume/partials/{generic_name}-form.html', context)
