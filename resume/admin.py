from django.contrib import admin

from resume.models import Resume, ResumeHeader, ResumeJob, ResumeProfessionalSummary, ResumeSkill

# Register your models here.
admin.site.register(ResumeHeader)
admin.site.register(ResumeSkill)
admin.site.register(ResumeJob)
admin.site.register(ResumeProfessionalSummary)
admin.site.register(Resume)