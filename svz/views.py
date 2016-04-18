# coding: utf-8

from django.conf import settings
from django.core.mail import send_mass_mail
from django.db import IntegrityError
from django.forms import (Form, CharField, TextInput, Textarea, Select,
                          ChoiceField)
from django.views.generic import TemplateView, FormView
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _

from .models import Player, Sponsor, Gazette, Reward, Rule

from rest_framework import serializers, viewsets, status
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import (RetrieveAPIView, CreateAPIView,
                                     ListAPIView, )


class MailForm(Form):
    TO_BOOL = {
        "1": None,
        "2": True,
        "3": False
    }

    DISPLAY_FORM = {
        "1": "Tous",
        "2": "Zombies",
        "3": "Humains"
    }

    title = CharField(max_length=100, widget=TextInput(
        attrs={'placeholder': _("Titre"), 'id': 'mail_title'}))

    content = CharField(max_length=10000,
                        widget=Textarea(attrs={'placeholder': _("Contenu"),
                                               'id': 'mail_content'}))
    target = ChoiceField(choices=DISPLAY_FORM.items(),
                         widget=Select(attrs={'id': "mail_target"}))

    def send_mail(self):
        zombie = self.TO_BOOL[self.cleaned_data['target']]
        users = (Player.objects.filter(zombie=zombie).filter(email__isnull=False)
                 if zombie is not None else Player.objects.all())
        bcc = [user.email for user in users]
        content = self.cleaned_data['content']
        title = self.cleaned_data['title']

        if zombie is None:
            print("Sending to ALL!")
        elif zombie:
            print("Sending to zombies!")
        else:
            print("Sending to humans")

        messages = []
        for mail in bcc:
            message = (title, content, settings.DEFAULT_FROM_EMAIL, [mail])
            messages.append(message)
        send_mass_mail(messages)


class SendMailView(APIView):
    authentication_classes = (SessionAuthentication, )
    permission_classes = (IsAdminUser, )

    def post(self, request, format=None):
        mail_form = MailForm({
            'title': request.POST.get('title'),
            'content': request.POST.get('content'),
            'target': request.POST.get('target'),
        })

        if mail_form.is_valid():
            mail_form.send_mail()
            return Response({'detail': "Okay!"}, status=status.HTTP_200_OK)
        return Response({'detail': mail_form.errors},
                        status=status.HTTP_400_BAD_REQUEST)


class POSTMultipleFieldLookupMixin(object):
    def get_object(self):
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.request.POST.get(field)
        return get_object_or_404(queryset, **filter)


class MultipleFieldLookupMixin(object):
    def get_object(self):
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]
        return get_object_or_404(queryset, **filter)


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ('sciper', 'name', 'email', 'contaminations', 'zombie',
                  'token_spent')


class PlayerTokenSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        return Player(**validated_data)

    def update(self, instance, validated_data):
        instance.token_spent += validated_data.get('token_spent', 0)
        instance.zombie = validated_data.get('zombify', instance.zombie)
        instance.save()
        return instance

    class Meta:
        model = Player
        fields = ('sciper', 'token_spent', 'zombie')


class PlayerCreateView(CreateAPIView):
    model = Player
    authentication_classes = (SessionAuthentication, )
    permission_classes = (IsAdminUser, )

    def post(self, request, *args, **kwargs):
        try:
            return super(PlayerCreateView, self).post(request, *args, **kwargs)
        except IntegrityError:
            content = {"detail": _("Ce sciper existe déjà !")}
            return Response(content, status=status.HTTP_409_CONFLICT)


class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    authentication_classes = (SessionAuthentication, )
    permission_classes = (IsAdminUser, )


class PlayerFilterListView(ListAPIView):
    authentication_classes = (SessionAuthentication, )
    permission_classes = (IsAdminUser, )

    def get(self, request, format=None):
        name = self.kwargs['name']
        queryset = Player.objects.filter(name__contains=name)
        return Response(queryset)


class AdminView(FormView):
    """
    Main view displaying admin panel
    """
    template_name = 'svz/admin.html'
    form_class = MailForm
    context_object_name = 'mail_form'


class InfoView(TemplateView):
    template_name = 'svz/index.html'

    def get_context_data(self):
        context = super(InfoView, self).get_context_data()
        context['sponsors'] = Sponsor.objects.all()
        context['gazettes'] = Gazette.objects.all()
        context['rewards'] = Reward.objects.all().order_by('?')
        context['rules'] = Rule.objects.all()
        return context


class PlayerFindView(MultipleFieldLookupMixin, RetrieveAPIView):
    model = Player
    lookup_fields = ('sciper', )

    serializer_class = PlayerSerializer

    authentication_classes = (SessionAuthentication, )
    permission_classes = (IsAdminUser, )

    def get_queryset(self):
        return Player.objects.all()


def score(player):
    A = 3
    B = 1
    return player.token_spent * B + player.contaminations * A


def player_compare(x, y):
    return score(x) - score(y)


class RankingView(ListAPIView):
    serializer_class = PlayerSerializer

    def get_queryset(self):
        players = Player.objects.order_by('-contaminations', '-token_spent')
        sorted(players, player_compare)
        return players[:10]
