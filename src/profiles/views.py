from django.shortcuts import render,get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.http import Http404
from django.contrib.auth.models import User
from django.views.generic import CreateView,View, DetailView,UpdateView
from django.shortcuts import redirect
from .forms import RegistrationForm
from .models import Profile


def activate_user_view(request, code=None, *args, **kwargs):
    if code:
        qs = Profile.objects.filter(activation_key=code)
        # print(qs)
        if qs.exists() and qs.count() == 1:
            profile = qs.first()
            # print(profile)
            if not profile.activated:
                user_ = profile.user
                # print(user_)
                user_.is_active = True
                user_.save()
                profile.activated = True
                profile.activation_key = None
                profile.save()
                return redirect("/login")
    # invalid code
    return redirect("/login")


class RegisterCreateView(CreateView):
    form_class = RegistrationForm
    template_name = 'registration/register.html'
    success_url = '/'

    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated():
            return redirect('/login')
        return super(RegisterCreateView, self).dispatch(*args, **kwargs)


class ProfileView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = request.user
        followers = user.profile.followers.all()
        following = user.is_following.all()
        return render(request, template_name='profiles/profile-view.html', context={'user': user,
                                                                                    'followers': followers,
                                                                                    'following': following
                                                                                    })


class ProfileUpdateView(UpdateView):
    model = Profile
    fields = ['first_name', 'last_name', 'bio', 'city', 'phone']
    template_name = 'profiles/profile_update.html'
    success_url = reverse_lazy('profile-view')

    def get_queryset(self):
        qs = Profile.objects.filter(user=self.request.user)
        return qs


class ProfileFollowToggle(LoginRequiredMixin, View):
    def post(self,request,*args, **kwargs):
        # print(request.POST)
        user_to_toggle = request.POST.get('username')
        print(user_to_toggle)
        profile_=Profile.objects.get(user__username__iexact=user_to_toggle)
        user = request.user
        if user in profile_.followers.all():
            profile_.followers.remove(user)
        else:
            profile_.followers.add(user)
        return redirect('/{}'.format(profile_.user.username))


class ProfileDetailView(DetailView):
    queryset = User.objects.filter(is_active=True)
    # print(queryset)
    template_name = 'profiles/user.html'

    def get_object(self):
        username = self.kwargs.get('username')
        if username is None:
            raise Http404
        return get_object_or_404(User, username__iexact=username, is_active=True)

    def get_context_data(self, *args, **kwargs):
        context = super(ProfileDetailView, self).get_context_data(*args, **kwargs)
        print(context)
        user = context['user']
        is_following = False
        if user.profile in self.request.user.is_following.all():
            is_following = True
        context['is_following'] = is_following
        return context





