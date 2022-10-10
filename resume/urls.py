
from django.urls import path

from resume.views import create_courses_view, create_header_view, create_jobs_view, create_professional_summary_view, create_skills_view, create_update_courses_hx_view, create_update_jobs_hx_view, create_update_skills_hx_view, delete_course_hx_view, delete_job_hx_view, delete_resume_hx_view, delete_skill_hx_view, edit_header_view, edit_professional_summary_view, generate_pdf, index_view

app_name = 'resume'

urlpatterns = [
    path('', index_view, name='index'),

    path('generate_pdf/<int:resume_id>', generate_pdf, name='generate-pdf'),

    path('hx/<int:resume_id>/delete/', delete_resume_hx_view, name='hx-resume-delete'),

    path('create/header/', create_header_view, name='create-header'),
    path('<int:resume_id>/edit/header/', edit_header_view, name='edit-header'),

    path('<int:resume_id>/edit/professional_summary/', edit_professional_summary_view, name='edit-professional-summary'),
    path('<int:resume_id>/create/professional_summary/', create_professional_summary_view, name='create-professional-summary'),

    path('<int:resume_id>/skills/', create_skills_view, name='create-skills'),
    path('hx/<int:resume_id>/skill/<int:object_id>', create_update_skills_hx_view, name='hx-skill-edit'),
    path('hx/<int:resume_id>/skill/', create_update_skills_hx_view, name='hx-skill-new'),
    path('hx/delete/<int:resume_id>/skill/<int:object_id>', delete_skill_hx_view, name='hx-skill-delete'),

    path('<int:resume_id>/jobs/', create_jobs_view, name='create-jobs'),
    path('hx/<int:resume_id>/job/<int:object_id>', create_update_jobs_hx_view, name='hx-job-edit'),
    path('hx/<int:resume_id>/job/', create_update_jobs_hx_view, name='hx-job-new'),
    path('hx/delete/<int:resume_id>/job/<int:object_id>', delete_job_hx_view, name='hx-job-delete'),

    path('<int:resume_id>/courses/', create_courses_view, name='create-courses'),
    path('hx/<int:resume_id>/course/<int:object_id>', create_update_courses_hx_view, name='hx-course-edit'),
    path('hx/<int:resume_id>/course/', create_update_courses_hx_view, name='hx-course-new'),   
    path('hx/delete/<int:resume_id>/course/<int:object_id>', delete_course_hx_view, name='hx-course-delete'),
]