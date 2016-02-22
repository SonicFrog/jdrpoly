# coding: utf-8

from django.db.models import Q
from django.http import JsonResponse
from django.views.generic.detail import BaseDetailView
from django.views.generic import (UpdateView, TemplateView,
                                  ListView)

from members.views import StaffRequiredMixin, LoginRequiredMixin
from .models import Player


def get_player(pk):
    return Player.objects().get(pk=pk)


def update_context(view, key, value):
    context = view.get_context_data()
    context[key] = value
    return context


class JsonResponseMixin(object):
    def render_to_Json_response(self, context, **response_kwargs):
        return JsonResponse(
            self.get_data(context),
            **response_kwargs
        )

    def get_data(self, context):
        return context


class JsonView(JsonResponseMixin, TemplateView):
    def render_to_error(self, message, **kwargs):
        context = update_context(self, 'message', message)
        context['error'] = True
        return self.render_to_Json_response(context, **kwargs)

    def render_to_response(self, context, **response_kwargs):
        return self.render_to_Json_response(context, **response_kwargs)


class JsonDetailView(JsonResponseMixin, BaseDetailView):
    def render_to_response(self, context, **kwargs):
        return self.render_to_Json_response(context, **kwargs)


class AdminView(LoginRequiredMixin, TemplateView):
    """
    Main view displaying admin panel
    """
    template_name = 'svz/admin.html'


class InfoView(TemplateView):
    template_name = 'svz/main.html'


class ContaminateView(StaffRequiredMixin, JsonView):
    """
    View used to contaminate a player and return Json values
    """
    def post(self, request, *args, **kwargs):
        pk1 = request.POST.get('player')
        pk2 = request.POST.get('target')
        contaminator = get_player(pk1)
        contaminated = get_player(pk2)
        context = self.get_context_data()

        if contaminator.has_contaminated(contaminated):
            context['message'] = "Contamination réussie !"
        else:
            return self.render_to_error("Contamination impossible !", **kwargs)
        return self.render_to_response(context, **kwargs)


class ReviveView(StaffRequiredMixin, JsonView):
    """
    View used to revive a player and return Json
    """
    def post(self, request, *args, **kwargs):
        message = "Joueur soigné !"
        pk = request.POST.get('pk')
        player = get_player(pk)

        if not player.revive():
            return self.render_to_error("Ce joueur n'est pas un zombie !",
                                        **kwargs)

        context = update_context(self, 'message', message)
        return self.render_to_response(context, **kwargs)


class TokenView(StaffRequiredMixin, JsonResponseMixin, UpdateView):
    """
    View used with AJAX to spend token for a player
    """
    model = Player

    def post(self, request, *args, **kwargs):
        player = self.get_object()
        count = self.request.POST.get('count')
        new_count = player.spend_token(count)
        context = update_context(self, 'token', new_count)
        return self.render_to_response(context, **kwargs)


class RegisterPlayerView(StaffRequiredMixin, JsonView):
    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        sciper = request.POST.get('sciper')
        Player.create(name, sciper)
        context = update_context(self, 'message', "Joueur créé !")
        return self.render_to_response(context, **kwargs)


class JsonPlayerView(StaffRequiredMixin, JsonDetailView):
    model = Player


class JsonPlayerFindView(StaffRequiredMixin, JsonResponseMixin, ListView):
    model = Player

    def get_queryset(self):
        name = self.kwargs['name']
        sciper = self.kwargs['sciper']
        restrict = Q(name__startswith=name) | Q(sciper=sciper)
        return Player.objects().filter(restrict)
