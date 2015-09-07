# coding: utf-8

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required, login_required
from django.views.generic import (DetailView, CreateView, FormView,
                                  View)
from django.forms import (Form, CharField, MultipleChoiceField,
                          EmailField, ImageField)
from django.forms.models import model_to_dict
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth.forms import (UserCreationForm, PasswordChangeForm)
from django.utils.timezone import datetime

import datetime as dt
import logging

from .models import Member, Code


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.FileHandler("error.log"))


class LoginRequiredMixin:
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)


class ProfileEditForm(Form):
    location = CharField(max_length=100, required=False)
    first_name = CharField(max_length=60, required=False)
    last_name = CharField(max_length=60, required=False)
    email = EmailField(max_length=255, required=True)
    image = ImageField(required=False)

    def __init__(self, instance=None):
        _initial = model_to_dict(instance) if instance is not None else {}
        if instance is not None:
            _initial.update(model_to_dict(instance.profile))
        super(ProfileEditForm, self).__init__(initial=_initial)

    def save(self, user):
        if not self.is_valid():
            return
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.profile.location = self.cleaned_data['location']
        user.profile.image = self.cleaned_data['image']
        user.save()
        user.profile.save()


class CodeCreationForm(Form):
    semesters = MultipleChoiceField(choices=Code.CHOICES)


class CodeUseForm(Form):
    content = CharField(max_length=30)

    def is_valid(self):
        if not super(CodeUseForm, self).is_valid():
            return False
        try:
            Code.objects.get(content=self.cleaned_data['content'])
        except:
            return False
        return True


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


class UserEditView(FormView, LoginRequiredMixin):
    """
    View pour l'édition d'un profil utilisateur
    """
    form_class = ProfileEditForm
    success_url = reverse_lazy('user-profile-view')
    template_name = 'members/edit.html'
    context_object_name = 'user_form'

    def get_form(self):
        return ProfileEditForm(instance=self.request.user)

    def form_valid(self, form):
        form.save(self.request.user)
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

    def form_invalid(self, form):
        logger.error("Form invalid!")
        return super(CodeUseView, self).form_invalid(form)

    def form_valid(self, form):
        now = datetime.now()
        code = Code.objects.get(content=form.cleaned_data['content'])

        until_date = None
        year = now.year

        if now.month >= 2 and now.month < 9:
            month = 10
            day = 1
        elif now.month >= 9:
            month = 2
            day = 28
            year = year + 1
        elif now.month < 2:
            month = 10

        until_date = dt.date(year, month, day)

        logger.info("Subscription now valid until ", until_date)

        self.get_object().profile.until = until_date

        self.get_object().profile.save()

        code.delete()

        return super(CodeUseView, self).form_valid(form)


class CodeCreationView(CreateView, LoginRequiredMixin):
    form_class = CodeCreationForm

    template_name = 'members/code.html'

    @method_decorator(permission_required('members.can_make_code'))
    def dispatch(self, *args, **kwargs):
        return super(CodeCreationView, self).dispatch(*args, **kwargs)
