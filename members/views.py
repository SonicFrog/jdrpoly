# coding: utf-8

from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic import (DetailView, CreateView, FormView,
                                  View, UpdateView, TemplateView)
from django.conf import settings
from django.core.mail import send_mail
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth.forms import (UserCreationForm, PasswordChangeForm)
from django.contrib.admin.views.decorators import staff_member_required
from django.template import Context
from django.template.loader import get_template
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _

from .models import Member, Code, user_is_staff
from .forms import CodeCreationForm, CodeUseForm


def user_is_member_decorator(user):
    return user.profile.is_member()


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)


class StaffRequiredMixin(object):
    @staff_member_required
    def dispatch(self, *args, **kwargs):
        return super(StaffRequiredMixin, self).dispatch(*args, **kwargs)


class MembershipRequiredMixin(LoginRequiredMixin):
    @method_decorator(user_passes_test(user_is_member_decorator))
    def dispatch(self, *args, **kwargs):
        return super(MembershipRequiredMixin, self).dispatch(*args, **kwargs)


class MainMemberView(LoginRequiredMixin, TemplateView):
    template_name = 'members/main.html'


class PasswordChangeView(LoginRequiredMixin, FormView):
    """
    View pour changer le mot de passe de l'utilisateur actif
    """
    success_url = reverse_lazy('user-password-ok')
    template_name = 'members/password_change.html'

    def get_form(self):
        return PasswordChangeForm(self.request.user)


class PasswordChangeOkView(LoginRequiredMixin, View):
    template_name = 'members/password_change_ok.html'


class UserProfileView(LoginRequiredMixin, DetailView):
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


class UserUpdateView(LoginRequiredMixin, UpdateView):
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


class CodeUseView(LoginRequiredMixin, FormView):
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


class CodeCreateView(LoginRequiredMixin, FormView):
    template_name = 'members/code.html'
    form_class = CodeCreationForm
    success_url = reverse_lazy('create-code')

    @method_decorator(user_passes_test(user_is_staff))
    def dispatch(self, *args, **kwargs):
        return super(CodeCreateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        title = _("Inscription JDR-poly")
        to = form.cleaned_data['email']
        code = Code.generate(form.cleaned_data['semesters'])
        template = get_template('members/code_mail.txt')
        data = Context({'code': code})
        mail_content = template.render(data)

        send_mail(title, mail_content, settings.DEFAULT_FROM_EMAIL, (to, ))

        return super(CodeCreateView, self).form_valid(form)
