from django.conf.urls import url
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.views import (password_change, password_change_done,
                                       login, logout, password_reset)
from .views import (UserProfileView, UserEditView, SelfProfileView,
                    UserCreateView, PasswordChangeView, CodeUseView)

urlpatterns = [
    url(r'^$', SelfProfileView.as_view(), name='user-profile-view'),
    url(r'^login$', login, name='login'),
    url(r'^edit$', UserEditView.as_view(), name='user-profile-edit'),
    url(r'^create$', UserCreateView.as_view(), name='user-create'),
    url(r'^password_reset/$', password_reset, name='password_reset',
        kwargs={'post_reset_redirect': reverse_lazy('login'),
                'template_name': 'members/password_reset.html'}),
    url(r'^password/$', password_change, name='user-password',
        kwargs={'template_name': 'members/password_change.html',
                'post_change_redirect': reverse_lazy('user-password-ok')}),
    url(r'^password_done/$', password_change_done, name='user-password-ok',
        kwargs={'template_name': 'members/password_change_ok.html'}),
    url(r'^logout$', logout, name='logout',
        kwargs={'success_url': reverse_lazy('login')}),
    url(r'^(?P<pk>\d+)$', UserProfileView.as_view(),
        name='other-user-profile'),
    url(r'^code$', CodeUseView.as_view(), name='use-code'),
]
