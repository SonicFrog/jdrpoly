from django.core import mail
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from django.test import TestCase, Client

from datetime import timedelta
from .views import NewsletterForm, ContactForm


class NewsletterFormTestCase(TestCase):
    """
    FIXME: These tests assume the in-memory email backend is used!
    """

    TEST_SUBJECT = 'Newsletter subject'
    TEST_CONTENT = """ Haha this is the newsletter
    multiline!
    """
    TEST_TO = 'test@example.com'

    TEST_TO_MEMBER = 'test@test.com'

    def setUp(self):
        self.user = User(username='haha', email=self.TEST_TO)
        self.user.save()
        self.user.profile.wants_newsletter = True
        self.user.profile.save()
        self.user2 = User(username='test', email=self.TEST_TO_MEMBER)
        self.user2.save()
        self.user2.profile.until = timezone.now() + timedelta(days=1)
        self.user2.profile.wants_newsletter = True
        self.user2.profile.save()

    def tearDown(self):
        self.user.delete()
        self.user2.delete()

    def test_member_only_newsletter_does_not_reach_non_members(self):
        form = NewsletterForm({'subject': self.TEST_SUBJECT,
                               'content': self.TEST_CONTENT,
                               'member_only': True})
        member_cnt = User.objects.filter(profile__until__gt=timezone.now()).count()
        self.assertTrue(form.is_valid())
        to = form.send_mail()
        self.assertEqual(len(to),
                         member_cnt)
        self.assertNotIn(self.TEST_TO, to)

    def test_member_only_newsletter_reaches_members(self):
        form = NewsletterForm({'subject': self.TEST_SUBJECT,
                               'content': self.TEST_CONTENT,
                               'member_only': True})
        self.assertTrue(form.is_valid())
        to = form.send_mail()
        self.assertEqual(len(to), 1)
        self.assertIn(self.TEST_TO_MEMBER, to)

    def test_all_members_receive_newsletter(self):
        form = NewsletterForm({'subject': self.TEST_SUBJECT,
                               'content': self.TEST_CONTENT,
                               'member_only': False})
        self.assertTrue(form.is_valid())
        self.assertFalse(form.cleaned_data['member_only'])
        to = form.send_mail()
        self.assertEqual(len(to), User.objects.all().count())
        self.assertIn(self.TEST_TO, to)
        self.assertIn(self.TEST_TO_MEMBER, to)

    def test_empty_subject(self):
        form = NewsletterForm({'subject': '', 'content': self.TEST_CONTENT})
        self.assertFalse(form.is_valid())

    def test_empty_content(self):
        form = NewsletterForm({'content': '', 'subject': self.TEST_SUBJECT})
        self.assertFalse(form.is_valid())


class NewsletterSendViewTestCase(TestCase):
    USERNAME = 'username'
    PASSWORD = 'password'
    EMAIL = 'test@example.com'

    SUBJECT = 'Hi'
    CONTENT = 'Newsletter content'

    def setUp(self):
        self.client = Client()
        self.user = User(username=self.USERNAME, email=self.EMAIL)
        self.user.set_password(self.PASSWORD)
        self.user.is_staff = True
        self.user.save()
        self.user.profile.wants_newsletter = True
        self.client.login(username=self.USERNAME, password=self.PASSWORD)

    def tearDown(self):
        self.user.delete()

    def test_admin_can_send_newsletter(self):
        response = self.client.post(reverse('newsletter-send'),
                                    {'subject': self.SUBJECT,
                                     'content': self.CONTENT,
                                     'member_only': False})
        news_num = User.objects.filter(profile__wants_newsletter=True).count()
        self.assertRedirects(response, reverse('newsletter-success'))
        self.assertEqual(len(mail.outbox),
                         news_num)
        self.assertEqual(mail.outbox[0].body, self.CONTENT)
        self.assertIn(self.EMAIL, mail.outbox[0].to)


class ContactFormTestCase(TestCase):
    CONTACT_NAME = 'Some dude'
    CONTACT_CONTENT = 'Hehe, im the message'
    CONTACT_EMAIL = 'some@dude.net'

    def test_form_accepts_valid_input(self):
        form = ContactForm({'name': self.CONTACT_NAME,
                            'email': self.CONTACT_EMAIL,
                            'message': self.CONTACT_CONTENT})
        self.assertTrue(form.is_valid())
        form.send_mail()
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn(self.CONTACT_EMAIL, mail.outbox[0].from_email)
        self.assertIn(self.CONTACT_NAME, mail.outbox[0].from_email)
        self.assertEqual(self.CONTACT_CONTENT, mail.outbox[0].body)
