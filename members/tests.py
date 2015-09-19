from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from django.utils import timezone

import datetime
import hashlib
import random
import string

from .models import Code
from .views import ProfileEditForm, CodeUseForm, UserEditView, CodeUseView


class AuthenticatedTestCase(TestCase):
    USERNAME = 'hello'
    PASSWORD = 'haha'
    FIRST_NAME = 'Ogier'
    EMAIL = 'aaaaa@bbbbbb.ch'
    LAST_NAME = 'Bouvier'

    CURRENT_END_DATE = datetime.date(2015, 4, 12)

    def setUp(self):
        self.user = User(username=self.USERNAME, first_name=self.FIRST_NAME,
                         email=self.EMAIL, last_name=self.LAST_NAME)
        self.user.set_password(self.PASSWORD)
        self.user.save()

    def tearDown(self):
        self.user.delete()

    def makeAuthRequest(self, path, method, data={}):
        request = method(path, data)
        request.user = self.user
        return request

    def reset_user(self):
        self.user.profile.until = self.CURRENT_END_DATE


class ProfileEditFormTestCase(AuthenticatedTestCase):
    def test_valid_data(self):
        form = ProfileEditForm({'email': self.EMAIL,
                                'first_name': self.FIRST_NAME,
                                'last_name': self.LAST_NAME},
                               instance=self.user, )
        if not form.is_valid():
            print(form.errors)
            self.fail(msg='form is not valid!')

        form.save()
        self.assertEqual(self.user.email, self.EMAIL)

    def test_no_email(self):
        form = ProfileEditForm(instance=self.user)
        form.fields['first_name'] = self.FIRST_NAME
        form.fields['last_name'] = self.LAST_NAME
        self.assertFalse(form.is_valid())

    def test_blank_data(self):
        form = ProfileEditForm()
        self.assertFalse(form.is_valid())


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


class CodeUseBehaviorTestCase(TestCase):
    """
    TODO: implement this test case
    """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_one_semester_code_correct(self):
        pass


def setup_view(view, request, *args, **kwargs):
    view.request = request
    view.args = args
    view.kwargs = kwargs
    return view


def randomchr():
    return chr(random.randint(0, 255))


def randomword(length):
    return ''.join([randomchr() for i in range(0, length)])


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
