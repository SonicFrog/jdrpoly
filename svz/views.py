# coding: utf-8

from django.db import IntegrityError
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _

from members.views import StaffRequiredMixin, LoginRequiredMixin
from .models import Player

from rest_framework import serializers, viewsets, views, status
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.generics import (UpdateAPIView, RetrieveAPIView,
                                     CreateAPIView)


def get_player(pk):
    return Player.objects().get(pk=pk)


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
        fields = ('sciper', 'name', 'contaminations', 'zombie', 'token_spent')


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


class AdminView(LoginRequiredMixin, TemplateView):
    """
    Main view displaying admin panel
    """
    template_name = 'svz/admin.html'


class InfoView(TemplateView):
    template_name = 'svz/index.html'


class ContaminateView(StaffRequiredMixin, views.APIView):
    """
    View used to contaminate a player and return Json values
    """

    authentication_classes = (SessionAuthentication, )
    permission_classes = (IsAdminUser, )

    def post(self, request, *args, **kwargs):
        pk1 = request.POST.get('player')
        pk2 = request.POST.get('target')
        contaminator = get_player(pk1)
        contaminated = get_player(pk2)

        if not contaminator.has_contaminated(contaminated):
            raise ValueError("")
        return super(ContaminateView, self).post(request, *args, **kwargs)


class TokenView(StaffRequiredMixin, UpdateAPIView):
    """
    View used with AJAX to spend token for a player
    """
    model = Player

    authentication_classes = (SessionAuthentication, )
    permission_classes = (IsAdminUser, )

    def perform_update(self, serializer):
        old_player = self.get_object()
        new_player = serializer.save()
        old_player.spend_token(new_player.token)
        old_player.save()


class PlayerFindView(MultipleFieldLookupMixin, RetrieveAPIView):
    model = Player
    lookup_fields = ('sciper', )

    serializer_class = PlayerSerializer

    authentication_classes = (SessionAuthentication, )
    permission_classes = (IsAdminUser, )

    def get_queryset(self):
        return Player.objects.all()
