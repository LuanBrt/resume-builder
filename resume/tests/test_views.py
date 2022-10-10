from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from resume.forms import ResumeHeaderForm, ResumeSummaryForm
from resume.models import Resume, ResumeHeader

class ResumeFormViewsTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        header = ResumeHeader.objects.create(firstname='', lastname='', profession='')
        self.resume = Resume.objects.create(resume_header=header, user=self.user)

    def test_view_creation_page(self):
        response = self.client.get(reverse('resume:create-header'))
        form = response.context['form']
        self.assertIsInstance(form, ResumeHeaderForm)

    def test_summary_creation_page(self):
       response = self.client.get(reverse('resume:create-professional-summary', kwargs={'resume_id': self.resume.id}))
       form = response.context['form']
       self.assertIsInstance(form, ResumeSummaryForm)

        

    
