from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils import timezone

from .models import Code
from .views import ProfileEditForm, CodeUseForm


class ProfileEditFormTestCase(TestCase):
    USERNAME = 'hello'
    PASSWORD = 'haha'
    FIRST_NAME = 'Ogier'
    EMAIL = 'aaaaa@bbbbbb.ch'
    LAST_NAME = 'Bouvier'
    LOCATION = 'Somewhere'

    def setUp(self):
        self.user = User(username=self.USERNAME)
        self.user.set_password(self.PASSWORD)
        self.user.first_name = self.FIRST_NAME
        self.user.last_name = self.LAST_NAME
        self.user.save()
        self.user.profile.location = None
        self.user.save()

    def tearDown(self):
        self.user.delete()

    def test_valid_data(self):
        form = ProfileEditForm(instance=self.user)
        form.fields['location'] = self.LOCATION
        form.fields['email'] = self.EMAIL

        if not form.is_valid():
            print(form.errors)
            self.fail(msg='form is not valid!')
        form.save(self.user)
        self.assertEqual(self.user.profile.location, self.LOCATION)
        self.assertEqual(self.user.email, self.EMAIL)

    def test_no_email(self):
        form = ProfileEditForm({'location': self.LOCATION,
                                'first_name': self.FIRST_NAME,
                                'last_name': self.LAST_NAME})
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


class CodeUseViewTestCase(TestCase):
    CODE_CONTENT = 'fowenoifwneoifnewoigbewfbsakj'
    CODE_CONTENT2 = 'fnwiunfoiewfoiewbfew'
    USER = 'ars3nic'
    PASSWORD = 'test_password'
    CLIENT = Client()

    def setUp(self):
        self.code1 = Code(content=self.CODE_CONTENT, semesters=1)
        self.code2 = Code(content=self.CODE_CONTENT2, semesters=2)
        self.code1.save()
        self.code2.save()
        self.user = User(username=self.USER)
        self.user.set_password(self.PASSWORD)
        self.user.save()
        self.client.login(user=self.USER, password=self.PASSWORD)

    def tearDown(self):
        self.code1.delete()
        self.code2.delete()

    def test_valid_code_1_semester(self):
        self.user.profile.until = now = timezone.now()
        response = self.CLIENT.post(reverse('use-code'),
                                    data={'content': self.CODE_CONTENT})
        self.assertEqual(response.status_code, 200)

        if now.month >= 9:
            self.assertGreater(self.user.profile.until.year, now.year)
        else:
            self.assertEqual(self.user.profile.until.year, now.year)

        if now.month >= 9:
            self.assertEqual(self.user.profile.until.month, 10)
        else:
            self.assertEqual(self.user.profile.until.month, 2)
