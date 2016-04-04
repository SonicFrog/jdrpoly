from django.conf.urls import url
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.views import (password_change, password_change_done,
                                       login, logout, password_reset,
                                       password_reset_complete,
                                       password_reset_done,
                                       password_reset_confirm)
from .views import (SelfProfileView, BugFreeProfileView,
                    UserCreateView, CodeUseView, UserUpdateView,
                    MainMemberView, CodeCreateView)

urlpatterns = [
    url(r'^$', MainMemberView.as_view(), name='user-main'),
    url(r'^profile/$', SelfProfileView.as_view(), name='user-profile-view'),
    url(r'^login$', login, name='login'),
    url(r'^edit$', UserUpdateView.as_view(), name='user-profile-edit'),
    url(r'^create$', UserCreateView.as_view(), name='user-create'),
    url(r'^password_reset/$', password_reset, name='password_reset',
        kwargs={'post_reset_redirect': reverse_lazy('login'),
                'template_name': 'members/password_reset.html'}),
    url(r'^password_reset_confirm/(?P<token>.+)/(?P<uidb64>.+)/$',
        password_reset_confirm, name='password_reset_confirm'),
    url(r'^password_reset_done/$', password_reset_done,
        name='password_reset_done'),
    url(r'^password_reset_complete/$', password_reset_complete,
        name='password_reset_complete'),
    url(r'^password/$', password_change, name='user-password',
        kwargs={'template_name': 'members/password_change.html',
                'post_change_redirect': reverse_lazy('user-password-ok')}),
    url(r'^password_done/$', password_change_done, name='user-password-ok',
        kwargs={'template_name': 'members/password_change_ok.html'}),
    url(r'^logout$', logout, name='logout',
        kwargs={'next_page': reverse_lazy('login')}),
    url(r'^view/(?P<slug>[-\w]+)$', BugFreeProfileView.as_view(),
        name='other-user-profile'),
    url(r'^code$', CodeUseView.as_view(), name='use-code'),
    url(r'^code-gen/$', CodeCreateView.as_view(), name='create-code'),
]
