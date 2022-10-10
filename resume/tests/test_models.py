
from django.test import TestCase
from django.contrib.auth.models import User

from resume.models import Resume, ResumeHeader, ResumeProfessionalSummary


class ResumeModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.header = ResumeHeader.objects.create(firstname='Tom', lastname='Test', profession='Tester')

        self.resume = Resume.objects.create(resume_header=self.header, user=self.user)

        self.summary = ResumeProfessionalSummary.objects.create(description='Tester summary')
        self.resume.resume_professional_summary = self.summary

        self.resume.save()

    def test_resume_deletion(self):
        self.resume.delete()
        header_qs = ResumeHeader.objects.all()
        summary_qs = ResumeProfessionalSummary.objects.all()
        self.assertFalse(header_qs.exists())
        self.assertFalse(summary_qs.exists())

    def test_optional_info(self):
        self.header.age = 60
        self.header.phone = '777-777-777'
        self.assertEqual(self.header.get_optional_info(), {'Age': 60, 'Phone': '777-777-777'})
        