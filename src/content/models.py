from django.db import models

# Create your models here.

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import post_save


class Blog(models.Model):
    author = models.ForeignKey(User)
    topic = models.CharField(max_length=500, null=True)
    title = models.CharField(max_length=500)
    body = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    # def get_absolute_url(self):
    #     return reverse('detail', kwargs={'pk': self.pk})


class Comment(models.Model):
    user = models.ForeignKey(User)
    blogs = models.ForeignKey(Blog, blank=True)
    comment_text = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.comment_text

class Vote(models.Model):
    user = models.ForeignKey(User)
    blog = models.ForeignKey(Blog)

    def __str__(self):
        return self.user


def post_save_user_receiver(sender, instance, created, *args, **kwargs):
    if created:
        is_active = True

    # if created:
    #     profile, is_created = Author.objects.get_or_create(user=instance)
    #     default_user_profile = Author.objects.get_or_create(user__id=1)[0]  # user__username=
    #     # default_user_profile.followers.add(instance)


post_save.connect(post_save_user_receiver, sender=User)
