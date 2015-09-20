from django.core.urlresolvers import reverse
from django.utils import timezone
from django.test import RequestFactory, Client, TestCase
from jdrpoly.tests.utils import AuthenticatedTestCase, randomword

from .models import Event, Edition
from .views import RegisterEditionView, UnregisterEditionView


def create_event_and_edition(member_only=False):
    name = randomword(20)
    event = Event(name=name, member_only=member_only)
    event.save()
    edition = Edition(date=timezone.now(), event=event)
    edition.save()
    return event


def extract_edition(event, pk):
    return event.editions.all()[pk]


class EventListViewTestCase(TestCase):
    TEST_EVENT_COUNT = 5

    def setUp(self):
        self.events = [create_event_and_edition()
                       for i in range(0, self.TEST_EVENT_COUNT)]
        self.client = Client()

    def tearDown(self):
        for e in self.events:
            e.delete()

    def test_event_list_correct_count(self):
        response = self.client.get(reverse('event-list'))
        self.assertEqual(self.TEST_EVENT_COUNT,
                         len(response.context_data['event_list']))

    def test_event_list_correct_pks(self):
        response = self.client.get(reverse('event-list'))

        self.assertEqual(response.status_code, 200)
        pk_list = [e.pk for e in response.context_data['event_list']]
        for event in self.events:
            self.assertIn(event.pk, pk_list)


class EventDetailViewTestCase(TestCase):
    def setUp(self):
        self.event = create_event_and_edition()

    def tearDown(self):
        self.event.delete()

    def test_displays_correct_event(self):
        response = self.client.get(reverse('event-detail',
                                           kwargs={'pk': self.event.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data['event'], self.event)

    def test_unknown_event(self):
        response = self.client.get(reverse('event-detail',
                                           kwargs={'pk': 26}))
        self.assertEqual(response.status_code, 404)


class RegisterEditionViewTestCase(AuthenticatedTestCase):
    def setUp(self):
        super(RegisterEditionViewTestCase, self).setUp()
        self.event = create_event_and_edition()

    def tearDown(self):
        super(RegisterEditionViewTestCase, self).tearDown()
        self.event.delete()

    def test_registers_correctly(self):
        view = RegisterEditionView.as_view()
        request = self.makeAuthRequest('dummy', RequestFactory().get)

        response = view(request, pk=self.event.pk)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(extract_edition(self.event, 0).participants.count(), 1)
        self.event.editions.all()[0].participants.remove(self.user)

    def test_registers_fail_not_logged_in(self):
        client = Client()
        response = client.get(reverse('edition-register',
                                      kwargs={'pk': self.event.pk}))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(extract_edition(self.event, 0).participants.count(), 0)


class UnregisterEditionViewTestCase(AuthenticatedTestCase):
    def setUp(self):
        super(UnregisterEditionViewTestCase, self).setUp()
        self.event = create_event_and_edition()
        self.event.editions.all()[0].participants.add(self.user)

    def test_unregisters_correctly(self):
        view = UnregisterEditionView.as_view()
        request = self.makeAuthRequest('dummy', RequestFactory().get)

        # Assert that user actually is registered for event
        self.assertEqual(self.event.editions.all()[0].participants.count(), 1)

        response = view(request, pk=self.event.pk)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.event.editions.all()[0].participants.count(), 0)
