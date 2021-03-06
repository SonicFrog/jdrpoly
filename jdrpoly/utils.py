from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

import datetime
import random


class AuthenticatedTestCase(TestCase):
    USERNAME = 'hello'
    PASSWORD = 'haha'
    FIRST_NAME = 'Ogier'
    EMAIL = 'aaaaa@bbbbbb.ch'
    LAST_NAME = 'Bouvier'

    CURRENT_END_DATE = datetime.date(2015, 4, 12)

    users = []

    def setUp(self):
        self.user = User(username=self.USERNAME, first_name=self.FIRST_NAME,
                         email=self.EMAIL, last_name=self.LAST_NAME)
        self.user.set_password(self.PASSWORD)
        self.user.save()
        self.user.profile.until = self.CURRENT_END_DATE
        self.user.profile.save()
        self.users = []

    def tearDown(self):
        self.user.delete()

        # Deleting users created by child TestCases
        for user in self.users:
            user.delete()

    def login(self, user):
        self.client.login(username=user.username, password=self.PASSWORD)

    def makeAuthRequest(self, path, method, data={}):
        request = method(path, data)
        request.user = self.user
        return request

    def makeMemberUser(self):
        user = self.makeUser()
        user.profile.until = (timezone.now() + datetime.timedelta(1)).date()
        user.profile.save()
        return user

    def makeUser(self):
        user = User(username=randomword(20))
        user.set_password(self.PASSWORD)
        user.save()
        user.profile.until = timezone.now().date()
        user.profile.save()
        self.users.append(user)
        return user

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


def randomsentence(wordcount):
    return ' '.join([randomword(10) for i in range(0, wordcount)])


def setup_view(view, request, *args, **kwargs):
    view.request = request
    view.args = args
    view.kwargs = kwargs
    return view
