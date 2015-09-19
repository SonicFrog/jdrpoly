from django.contrib.auth.models import User
from django.test import TestCase

import datetime
import random


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
        self.user.last_name = randomword(20)
        self.user.first_name = randomword(20)
        self.user.email = 'tete@tete.ch'
        self.user.save()


def randomchr():
    return chr(random.randint(0, 255))


def randomword(length):
    return ''.join([randomchr() for i in range(0, length)])


def setup_view(view, request, *args, **kwargs):
    view.request = request
    view.args = args
    view.kwargs = kwargs
    return view
