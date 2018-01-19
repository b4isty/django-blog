from django.conf.urls import url
from .views import BlogDetailView, BlogCreateView, BlogUpdateView, BlogDeleteView, BlogTopicListView

urlpatterns = [
    url(r'^(?P<pk>[0-9]+)/$', BlogDetailView.as_view(), name='detail'),
    url(r'^create/$', BlogCreateView.as_view(), name='create'),
    url(r'^(?P<pk>[0-9]+)/update/$', BlogUpdateView.as_view(), name='update'),
    url(r'^(?P<pk>[0-9]+)/delete/$', BlogDeleteView.as_view(), name='delete'),
    url(r'^technology/$', BlogTopicListView.as_view(), name='technology'),
    url(r'^music/$', BlogTopicListView.as_view(), name='music'),
]
