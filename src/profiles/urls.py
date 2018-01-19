from django.conf.urls import url
from .views import ProfileDetailView, ProfileUpdateView

urlpatterns = [
    url(r'^(?P<username>[\w-]+)/$', ProfileDetailView.as_view(), name='profile-detail'),
    url(r'^edit/(?P<pk>[0-9]+)/$',ProfileUpdateView.as_view(), name='edit')
]
