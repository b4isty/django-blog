from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from .utils import code_generator


class Profile(models.Model):
    user = models.OneToOneField(User)
    first_name = models.CharField(max_length=40, blank=True, null=True)
    last_name = models.CharField(max_length=40, blank=True, null=True)
    bio = models.TextField(null=True, blank=True)
    city = models.CharField(max_length=100, default='')
    phone = models.IntegerField(default=0)
    followers = models.ManyToManyField(User, related_name='is_following', blank=True)
    image = models.ImageField(blank=True,null=True)
    activation_key = models.CharField(max_length=120, blank=True, null=True)
    activated = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def send_activation_email(self):
        print('Activation')
        if not self.activated:
            self.activation_key = code_generator()  # gen key
            self.save()
            path_ = reverse('activate', kwargs={'code': self.activation_key})
            subject = 'Activate Account'
            from_email = settings.DEFAULT_FROM_EMAIL
            message = 'Activate your account here:{}'.format(path_)
            recipient_list = [self.user.email]
            html_message = '<p> Activate your account here:{}</p>'.format(path_)
            print(html_message)

            # sent_mail = send_mail(subject,
            #                       message,
            #                       from_email,
            #                       recipient_list,
            #                       fail_silently=False,
            #                       html_message=html_message
            #
            #                      )
            sent_mail = False
            return sent_mail


def post_save_user_receiver(sender, instance, created, *args, **kwargs):
    if created:
        print(kwargs)
        profile, is_created = Profile.objects.get_or_create(user=instance)
        default_user_profile = Profile.objects.get_or_create(user__id=2)[0]
        default_user_profile.followers.add(instance)
        profile.followers.add(default_user_profile.user)
        profile.followers.add(3)


post_save.connect(post_save_user_receiver, sender=User)