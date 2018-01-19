"""myblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from content.views import BlogListView
from profiles.views import RegisterCreateView, activate_user_view, ProfileView,ProfileFollowToggle
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', BlogListView.as_view(), name='home'),
    url(r'^content/', include('content.urls', namespace='content')),
    url(r'^profile/$', ProfileView.as_view(), name='profile-view'),
    url(r'^register/$', RegisterCreateView.as_view(), name='register'),
    url(r'^activate/(?P<code>[a-z0-9].*)/$', activate_user_view, name='activate'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^profile-follow/$', ProfileFollowToggle.as_view(), name='follow'),
    url(r'^', include('profiles.urls', namespace='profile')),

]
