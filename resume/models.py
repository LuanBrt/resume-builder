import os
import uuid
from django.db import models
from django.urls import reverse
from django.db.models.signals import post_delete, pre_save
from django.conf import settings


# The header of the Resume, contains all the personal information
class ResumeHeader(models.Model):

    def get_profile_picture_path(instance, filename):
        extension = filename.split('.')[-1]
        name = uuid.uuid4().hex
        return f'profile_pictures/{name}.{extension}'

    firstname = models.CharField(max_length=150)
    lastname = models.CharField(max_length=150)
    profession = models.CharField(max_length=150)
    profile_picture = models.ImageField(upload_to=get_profile_picture_path)

    age = models.SmallIntegerField(blank=True, null=True)
    city = models.CharField(max_length=150, blank=True, null=True)
    state = models.CharField(max_length=150, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(max_length=254, blank=True, null=True)

    def get_edit_url(self):
        return reverse('resume:edit-header', kwargs={'resume_id': self.resume.id})

    def get_optional_info(self):
        fields = {
             'Age': self.age,
             'City': self.city,
             'State': self.state,
             'Phone': self.phone,
             'Email': self.email
             }
        filled_fields = {}
        for k, v in fields.items():
            if v is not None:
                filled_fields[k] = v
        
        return filled_fields

# The summary of the Resume
class ResumeProfessionalSummary(models.Model):
    description = models.TextField()

    def get_edit_url(self):
        return reverse('resume:edit-professional-summary', kwargs={'resume_id': self.resume.id})
    
# The main resume class, wraps up every other section of the resume
class Resume(models.Model): 
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    resume_header = models.OneToOneField(ResumeHeader, on_delete=models.CASCADE)
    resume_professional_summary = models.OneToOneField(ResumeProfessionalSummary, blank=True, null=True, on_delete=models.CASCADE)

    def get_edit_url(self):
        return self.resume_header.get_edit_url()

    def get_delete_url(self):
        return reverse('resume:hx-resume-delete', kwargs={'resume_id': self.id})

    def get_skills_qs(self):
        return self.resumeskill_set.all()

    def get_jobs_qs(self):
        return self.resumejob_set.all()

    def get_courses_qs(self):
        return self.resumecourse_set.all()

# Used to represent the work history section of the resume
class ResumeJob(models.Model):
    parent_resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    occupation = models.CharField(max_length=150)
    company_name = models.CharField(max_length=150)
    entry_date = models.DateField(blank=True, null=True)
    leave_date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def get_edit_url(self):
        return reverse('resume:hx-job-edit', kwargs={'resume_id': self.parent_resume.id, 'object_id': self.id})

    def get_delete_url(self):
        return reverse('resume:hx-job-delete', kwargs={'resume_id': self.parent_resume.id, 'object_id': self.id})

# Used to represent the skills list section of the resume
class ResumeSkill(models.Model):

    BASIC = 1
    INTERMEDIATE = 2
    GOOD = 3
    VERY_GOOD = 4
    MASTER = 5

    RATING = (
        (BASIC, '★'),
        (INTERMEDIATE, '★★'),
        (GOOD, '★★★'),
        (VERY_GOOD, '★★★★'),
        (MASTER, '★★★★★')
    )

    parent_resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    skill_summary = models.CharField(max_length=150)
    rating = models.PositiveSmallIntegerField(choices=RATING)

    def get_edit_url(self):
        return reverse('resume:hx-skill-edit', kwargs={'resume_id': self.parent_resume.id, 'object_id': self.id})

    def get_delete_url(self):
        return reverse('resume:hx-skill-delete', kwargs={'resume_id': self.parent_resume.id, 'object_id': self.id})

    def get_rating_string(self):
        return self.RATING[self.rating-1][1]

# Used to represent the education section of the resume
class ResumeCourse(models.Model):
    parent_resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    major = models.CharField(max_length=150)
    college_name = models.CharField(max_length=150)
    entry_date = models.DateField(blank=True, null=True)
    leave_date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def get_edit_url(self):
        return reverse('resume:hx-course-edit', kwargs={'resume_id': self.parent_resume.id, 'object_id': self.id})

    def get_delete_url(self):
        return reverse('resume:hx-course-delete', kwargs={'resume_id': self.parent_resume.id, 'object_id': self.id})
# Used to delete all of the dependencies of a resume
def delete_related_dependencies(sender, instance, **kwargs):
    resume_header = instance.resume_header
    resume_professional_summary = instance.resume_professional_summary
    if resume_header is not None:
        resume_header.delete()
    if resume_professional_summary is not None:
        resume_professional_summary.delete()

# Functions used to delete images from the memory
def auto_delete_profile_picture(sender, instance, **kwargs):
    if instance.profile_picture:
        if os.path.isfile(instance.profile_picture.path):
            os.remove(instance.profile_picture.path)

def auto_delete_profile_picture_update(sender, instance, **kwargs):
    if not instance.id:
        return False

    try:
        old_picture = ResumeHeader.objects.get(id=instance.id).profile_picture
    except ResumeHeader.DoesNotExist:
        return False
    
    new_picture = instance.profile_picture
    if not old_picture == new_picture:
        if os.path.isfile(old_picture.path):
            os.remove(old_picture.path)
    
post_delete.connect(delete_related_dependencies, sender=Resume)
post_delete.connect(auto_delete_profile_picture, sender=ResumeHeader)
pre_save.connect(auto_delete_profile_picture_update, sender=ResumeHeader)