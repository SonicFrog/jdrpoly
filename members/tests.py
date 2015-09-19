from django.test import TestCase, RequestFactory
from django.utils import timezone

from jdrpoly.tests.utils import AuthenticatedTestCase, randomword
from .models import Code
from .views import CodeUseForm, CodeUseView, UserUpdateView


class CodeUseFormTestCase(TestCase):
    CODE_CONTENT = 'fffeeeeeffffffddddd'

    def setUp(self):
        self.code = Code(content=self.CODE_CONTENT, semesters=1)
        self.code.save()

    def tearDown(self):
        self.code.delete()

    def test_valid_code_is_valid_form(self):
        form = CodeUseForm({'content': self.CODE_CONTENT})
        self.assertTrue(form.is_valid())

    def test_invalid_code_is_invalid_form(self):
        form = CodeUseForm({'content': 'random_string'})
        self.assertFalse(form.is_valid())


class UserUpdateViewTestCase(AuthenticatedTestCase):
    def test_updates_user_profile(self):
        self.reset_user()
        request = self.makeAuthRequest('dummy', RequestFactory().post,
                                       data={'email': self.EMAIL,
                                             'first_name': self.FIRST_NAME,
                                             'last_name': self.LAST_NAME})
        view = UserUpdateView.as_view()
        response = view(request)

        # Thew view should redirect to profile view
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.user.first_name, self.FIRST_NAME)
        self.assertEqual(self.user.last_name, self.LAST_NAME)
        self.assertEqual(self.user.email, self.EMAIL)

    def test_requires_email(self):
        self.reset_user()
        request = self.makeAuthRequest('dummy', RequestFactory().post,
                                       data={'first_name': self.FIRST_NAME,
                                             'last_name': self.LAST_NAME})
        view = UserUpdateView.as_view()
        response = view(request)

        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(self.user.first_name, self.FIRST_NAME)


class CodeUseViewTestCase(AuthenticatedTestCase):
    def makeCode(self):
        content = randomword(30)
        code = Code(content=content, semesters=1)
        code.save()
        return content

    def test_invalid_code(self):
        self.reset_user()
        request = self.makeAuthRequest('fake', RequestFactory().post,
                                       {'content': 'ewfoewfiwbegiewbg'})
        view = CodeUseView.as_view()
        response = view(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.user.profile.until, self.CURRENT_END_DATE)

    def test_form_valid(self):
        now = timezone.now()
        code = self.makeCode()
        self.reset_user()
        view = CodeUseView()
        view.request = self.makeAuthRequest('dummy', RequestFactory().post,
                                            {'content': code})
        form = CodeUseForm({'content': code})
        self.assertTrue(form.is_valid())
        view.form_valid(form)

        if now.month < 9:
            self.assertEqual(self.user.profile.until.month, 10)
            self.assertEqual(self.user.profile.until.year, now.year)
        else:
            self.assertGreater(self.user.profile.until.year, now.year)
            self.assertEqual(self.user.profile.until.month, 2)

    def test_valid_code_1_semester(self):
        code = self.makeCode()
        self.reset_user()
        now = timezone.now()

        self.assertEqual(Code.objects.filter(content=code).count(), 1)

        view = CodeUseView.as_view()
        request = self.makeAuthRequest('dummy', RequestFactory().post,
                                       data={'content': code})
        response = view(request)

        # The view should redirect to success_url
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Code.objects.filter(content=code).count(), 0)

        if now.month < 9:
            self.assertEqual(self.user.profile.until.month, 10)
            self.assertEqual(self.user.profile.until.year, now.year)
        else:
            self.assertGreater(self.user.profile.until.year, now.year)
            self.assertEqual(self.user.profile.until.month, 2)
