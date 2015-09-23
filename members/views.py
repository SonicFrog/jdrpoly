# coding: utf-8

from django.contrib.auth.decorators import login_required
from django.views.generic import (DetailView, CreateView, FormView,
                                  View, UpdateView, TemplateView)
from django.forms import (Form, CharField, MultipleChoiceField, )

from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth.forms import (UserCreationForm, PasswordChangeForm)
from django.utils.timezone import datetime

import datetime as dt

from .models import Member, Code


class LoginRequiredMixin:
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)


class CodeCreationForm(Form):
    semesters = MultipleChoiceField(choices=Code.CHOICES)


class CodeUseForm(Form):
    content = CharField(max_length=30, label=False)

    def is_valid(self):
        if not super(CodeUseForm, self).is_valid():
            return False
        try:
            Code.objects.get(content=self.cleaned_data['content'])
        except:
            return False
        return True

    def save(self):
        pass


class MainMemberView(TemplateView, LoginRequiredMixin):
    template_name = 'members/main.html'


class PasswordChangeView(FormView, LoginRequiredMixin):
    """
    View pour changer le mot de passe de l'utilisateur actif
    """
    success_url = reverse_lazy('user-password-ok')
    template_name = 'members/password_change.html'

    def get_form(self):
        return PasswordChangeForm(self.request.user)


class PasswordChangeOkView(View, LoginRequiredMixin):
    template_name = 'members/password_change_ok.html'


class UserProfileView(DetailView, LoginRequiredMixin):
    """
    View pour voir le profil d'un utilisateur arbitraire
    """
    model = User
    template_name = 'members/view.html'
    context_object_name = 'member'


class SelfProfileView(UserProfileView):
    """
    View pour voir son propre profil utilisateur
    """
    def get_object(self):
        return self.request.user


class UserUpdateView(UpdateView, LoginRequiredMixin):
    model = User
    fields = ['email', 'first_name', 'last_name']
    success_url = reverse_lazy('user-profile-view')
    template_name = 'members/edit.html'

    def get_object(self):
        return self.request.user


class UserCreateView(CreateView):
    model = Member
    success_url = reverse_lazy('login')
    template_name = 'members/create.html'
    form_class = UserCreationForm


class CodeUseView(FormView, LoginRequiredMixin):
    """
    View pour utiliser un code sur un compte utilisateur
    """
    success_url = reverse_lazy('user-profile-view')
    template_name = 'members/code_use.html'
    form_class = CodeUseForm

    def form_valid(self, form):
        code = Code.objects.get(content=form.cleaned_data['content'])
        user = self.request.user

        code.use_for(user)

        return super(CodeUseView, self).form_valid(form)
