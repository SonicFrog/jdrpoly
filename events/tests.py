from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.test import RequestFactory, Client, TestCase
from jdrpoly.tests.utils import (AuthenticatedTestCase, randomword,
                                 randomsentence)

from random import randint

from .models import Event, Edition, Campaign
from .views import (RegisterEditionView, UnregisterEditionView,
                    CampaignCreateForm, CampaignPropositionView,)


def create_event_and_edition(member_only=False):
    name = randomword(20)
    event = Event(name=name, member_only=member_only)
    event.save()
    edition = Edition(date=timezone.now(), event=event)
    edition.save()
    return event


def extract_edition(event, pk):
    return event.editions.all()[pk]


def create_campaign(user):
    edition = extract_edition(create_event_and_edition(), 0)
    campaign = Campaign(max_players=randint(1, 12), open_for_registration=True,
                        running=True, description=randomsentence(15),
                        start=edition, owner=user, name=randomword(20))
    campaign.save()
    return campaign


class CampaignListViewTestCase(AuthenticatedTestCase):
    TEST_CAMPAIGN_COUNT = 10

    def setUp(self):
        super(CampaignListViewTestCase, self).setUp()
        self.campaigns = [create_campaign(self.user)
                          for i in range(0, self.TEST_CAMPAIGN_COUNT)]

    def tearDown(self):
        super(CampaignListViewTestCase, self).setUp()
        for c in self.campaigns:
            c.delete()

    def test_displays_correct_campaigns(self):
        response = self.client.get(reverse('campaign-list'))

        for c in self.campaigns:
            self.assertIn(c, response.context_data['campaign_list'])


class CampaignToggleEnrollViewTestCase(AuthenticatedTestCase):
    def setUp(self):
        super(CampaignToggleEnrollViewTestCase, self).setUp()
        self.user = self.makeMemberUser()
        self.user.save()
        self.campaign = create_campaign(self.user)
        self.login(self.user)

    def tearDown(self):
        super(CampaignToggleEnrollViewTestCase, self).tearDown()
        self.user.delete()
        self.campaign.delete()

    def test_unregisters(self):
        self.campaign.register_user(self.user)
        self.client.get(reverse('campaign-enroll',
                                kwargs={'pk': self.campaign.pk}))

        self.assertEqual(self.campaign.participants.all().count(), 0)
        self.campaign.delete()

    def test_registers(self):
        self.client.get(reverse('campaign-enroll',
                                kwargs={'pk': self.campaign.pk}))
        self.assertEqual(self.campaign.participants.all().count(), 1)
        self.campaign.unregister_user(self.user)

    def test_registers_then_unregisters(self):
        self.client.get(reverse('campaign-enroll',
                                kwargs={'pk': self.campaign.pk}))
        self.assertEqual(self.campaign.participants.all().count(), 1)
        self.client.get(reverse('campaign-enroll',
                                kwargs={'pk': self.campaign.pk}))
        self.assertEqual(self.campaign.participants.all().count(), 0)


class CampaignCreateFormTestCase(AuthenticatedTestCase):
    def setUp(self):
        super(CampaignCreateFormTestCase, self).setUp()
        self.event = create_event_and_edition()

    def tearDown(self):
        super(CampaignCreateFormTestCase, self).tearDown()
        self.event.delete()

    def test_empty_form_invalid(self):
        form = CampaignCreateForm()
        self.assertFalse(form.is_valid())

    def test_form_validates_correctly(self):
        form = CampaignCreateForm({'max_players': 10,
                                   'open_for_registration': True,
                                   'description': randomword(40),
                                   'running': True,
                                   'name': randomword(10),
                                   'owner': self.user,
                                   'start': extract_edition(self.event, 0).pk})
        self.assertTrue(form.is_valid())

    def test_negative_max_players_invalid(self):
        form = CampaignCreateForm({'max_players': -1,
                                   'open_for_registration': True,
                                   'description': randomword(40),
                                   'running': True,
                                   'name': randomword(10),
                                   'owner': self.user,
                                   'start': extract_edition(self.event, 0).pk})
        self.assertFalse(form.is_valid())


class CampaignPropositionViewTestCase(AuthenticatedTestCase):
    CORRECT_DATA = {'max_players': 10,
                    'open_for_registration': True,
                    'description': randomword(40),
                    'running': True,
                    'name': randomword(10),
                    'start': extract_edition(create_event_and_edition(), 0).pk}

    def setUp(self):
        super(CampaignPropositionViewTestCase, self).setUp()
        self.view = CampaignPropositionView.as_view()

    def fails_without_member_user(self):
        user = self.makeUser()
        self.client.login(username=user.username, password=self.PASSWORD)
        self.client.get(reverse('propose-campaign'), self.CORRECT_DATA)
        self.assertEqual(Campaign.objects.all().count(), 0)

    def test_creates_with_correct_user(self):
        request = self.makeAuthRequest('dummy', RequestFactory().get,
                                       self.CORRECT_DATA)
        self.assertEqual(Campaign.objects.all().count(), 0)

        self.view(request)
        self.assertEqual(Campaign.objects.all().count(), 1)
        self.assertEqual(Campaign.objects.get(pk=1).owner, self.user)
        Campaign.objects.get(pk=1).delete()

    def test_creates_correctly(self):
        self.client.login(username=self.user.username, password=self.PASSWORD)
        self.client.get(reverse('propose-campaign'),
                        data=self.CORRECT_DATA)

        self.assertEqual(Campaign.objects.all().count(), 1)
        Campaign.objects.all().delete()

    def test_no_creation_when_not_logged_in(self):
        self.client.get(reverse('propose-campaign'),
                        self.CORRECT_DATA)
        self.assertEqual(Campaign.objects.all().count(), 0)


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
        self.event_mbr = create_event_and_edition(member_only=True)
        self.event_mbr.save()

    def tearDown(self):
        super(RegisterEditionViewTestCase, self).tearDown()
        self.event.delete()
        self.event_mbr.delete()

    def test_registers_member_only_when_member(self):
        edition = extract_edition(self.event_mbr, 0)
        user = self.makeMemberUser()

        view = RegisterEditionView.as_view()
        request = RequestFactory().get('dummy')
        request.user = user

        response = view(request, pk=edition.pk)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(edition.participants.count(), 1)
        edition.participants.remove(user)

    def test_registers_member_only_fails_when_not_member(self):
        edition = extract_edition(self.event_mbr, 0)
        view = RegisterEditionView.as_view()
        request = RequestFactory().get('dummy')
        request.user = self.user

        response = view(request, pk=edition.pk)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(edition.participants.count(), 0)

    def test_registers_correctly_when_logged_in(self):
        view = RegisterEditionView.as_view()
        request = self.makeAuthRequest('dummy', RequestFactory().get)

        response = view(request, pk=self.event.pk)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(extract_edition(self.event, 0).participants.count(),
                         1)
        self.event.editions.all()[0].participants.remove(self.user)

    def test_registers_fail_not_logged_in(self):
        client = Client()
        response = client.get(reverse('edition-register',
                                      kwargs={'pk': self.event.pk}))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(extract_edition(self.event, 0).participants.count(),
                         0)


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


class CampaignModelTestCase(AuthenticatedTestCase):
    def setUp(self):
        self.good_user = self.makeMemberUser()
        self.bad_user = self.makeUser()
        self.campaign = create_campaign(self.good_user)

    def tearDown(self):
        self.good_user.delete()
        self.bad_user.delete()
        self.campaign.delete()

    def test_registers_member_user(self):
        self.campaign.register_user(self.good_user)
        self.assertEqual(self.campaign.participants.all().count(), 1)

    def test_does_not_register_non_member_user(self):
        self.campaign.register_user(self.bad_user)
        self.assertEqual(self.campaign.participants.all().count(), 0)

    def test_registers_then_unregisters(self):
        self.campaign.register_user(self.good_user)
        self.campaign.unregister_user(self.good_user)
        self.assertEqual(self.campaign.participants.all().count(), 0)
