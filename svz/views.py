# coding: utf-8

from django.views.generic import TemplateView
from django.utils.translation import ugettext_lazy as _

from members.views import StaffRequiredMixin, LoginRequiredMixin
from .models import Player

from rest_framework import serializers, viewsets, views


def get_player(pk):
    return Player.objects().get(pk=pk)


def update_context(view, key, value):
    context = view.get_context_data()
    context[key] = value
    return context


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ('sciper', 'name', 'contaminations', 'zombie',)


class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer


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
    def post(self, request, *args, **kwargs):
        pk1 = request.POST.get('player')
        pk2 = request.POST.get('target')
        contaminator = get_player(pk1)
        contaminated = get_player(pk2)
        context = self.get_context_data()

        if contaminator.has_contaminated(contaminated):
            context['message'] = _("Contamination réussie !")
        else:
            return self.render_to_error(_("Contamination impossible !"),
                                        **kwargs)

        return self.render_to_response(context, **kwargs)


class ReviveView(StaffRequiredMixin, views.APIView):
    """
    View used to revive a player and return Json
    """
    def post(self, request, *args, **kwargs):
        message = "Joueur soigné !"
        pk = request.POST.get('pk')
        player = get_player(pk)

        if not player.revive():
            return self.render_to_error(_("Ce joueur n'est pas un zombie !"),
                                        **kwargs)

        context = update_context(self, 'message', message)
        return self.render_to_response(context, **kwargs)


class TokenView(StaffRequiredMixin, views.APIView):
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


class PlayerFindView(views.APIView):

    def get_queryset(self):
        name = self.kwargs['name']
        return Player.objects().filter(name__startswith=name)
