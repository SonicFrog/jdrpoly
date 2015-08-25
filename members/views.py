# coding: utf-8

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required, login_required
from django.views.generic import (DetailView, CreateView, UpdateView, FormView,
                                  View)
from django.forms import ModelForm
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth.forms import (UserChangeForm, UserCreationForm,
                                       PasswordChangeForm)

from django.utils.timezone import datetime
import datetime as dt

from .models import Member, Code


class LoginRequiredMixin:
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)


class UserEditForm(UserChangeForm):
    class Meta:
        model = Member
        fields = ['image', 'location']


class CodeCreationForm(ModelForm):
    class Meta:
        model = Code
        fields = ['semesters']


class CodeUseForm(ModelForm):
    class Meta:
        model = Code
        fields = ['content']


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

    def get_context_data(self, **kwargs):
        context = super(UserProfileView, self).get_context_data()
        context['extended'] = Member.objects.filter(user=kwargs['object'])
        return context


class SelfProfileView(UserProfileView):
    """
    View pour voir son propre profil utilisateur
    """
    def get_object(self):
        return self.request.user


class UserEditView(UpdateView, LoginRequiredMixin):
    """
    View pour l'édition d'un profil utilisateur
    """
    form_class = UserEditForm

    template_name = 'members/edit.html'
    context_object_name = 'user_form'

    success_url = reverse_lazy('user-profile-view')

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        # TODO: code logic for editing user
        return super(UserEditView, self).form_valid(form)


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

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        try:
            code = Code.objects.get(content=form.content)
        except:
            return False

        now = datetime.now()
        delta = None

        if code.semesters is 1:
            delta = dt.timedelta(190)
        else:
            delta = dt.timedelta(380)

        start = None

        if now.month >= 9:
            # Subscription is valid until February
            start = dt.date(now.year, 2, 28)
        elif now.month < 2:
            # Subscriptions is valid until October
            start = dt.date(now.year, 10, 1)

        until_date = start + delta

        self.get_object().profile.until = until_date

        self.get_object().profile.save()

        return super(CodeUseView, self).form_valid(form)


class CodeCreationView(CreateView, LoginRequiredMixin):
    form_class = CodeCreationForm

    template_name = 'members/code.html'

    @method_decorator(permission_required('members.can_make_code'))
    def dispatch(self, *args, **kwargs):
        return super(CodeCreationView, self).dispatch(*args, **kwargs)
