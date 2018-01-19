from django.shortcuts import render
from django.views import View

from django.views.generic import DetailView, ListView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.views.generic.edit import CreateView
from django.core.urlresolvers import reverse_lazy
from .models import Blog, Vote, Comment


# from .forms import ContentForm


class BlogListView(ListView):
    # template_name = 'content/blog_list.html'
    model = Blog
    paginate_by = 7

    def post(self, request, *args, **kwargs):
        print(request.POST)
        if request.POST['type'] == 'vote':
            blog = Blog.objects.get(id=request.POST['blog_id'])
            if request.user.is_authenticated:
                if request.POST['vote'][:1] == 'U':
                    upvote = Vote.objects.get_or_create(blog=blog, user=request.user)
                elif request.POST['vote'][:1] == "D":
                    upvote = Vote.objects.filter(blog=blog, user=request.user).delete()

        return HttpResponseRedirect('/')

    def get_queryset(self):
        qs = Blog.objects.all().order_by("-updated")

        return qs


class BlogDetailView(DetailView):
    model = Blog
    template_name = 'content/blog_detail.html'

    # def get_queryset(self):
    #     abc = Blog.objects.all()
    #     return abc  # filter(author=self.request.user.author)

    def post(self, request, *args, **kwargs):
        blog = Blog.objects.get(id=request.POST['blog_id'])
        print(request.POST)
        if request.POST['type'] == 'comment':
            print(request.POST)
            comment = Comment.objects.update_or_create(blogs=blog, user=request.user, comment_text=request.POST['write'])

        return HttpResponseRedirect('/content/{}'.format(int(blog.id)))


class BlogCreateView(LoginRequiredMixin, CreateView):
    model = Blog
    fields = ['topic', 'title', 'body']
    success_url = '/'

    def get_queryset(self):
        qs = Blog.objects.filter(author=self.request.user)

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.author = self.request.user
        instance.save()
        return super(BlogCreateView, self).form_valid(form)


class BlogUpdateView(LoginRequiredMixin, UpdateView):
    model = Blog
    fields = ['title', 'body']
    template_name = 'content/blog_update_form.html'
    success_url = reverse_lazy('home')

    def get_queryset(self):
        qs = Blog.objects.filter(author=self.request.user)
        return qs


class BlogDeleteView(LoginRequiredMixin, DeleteView):
    model = Blog
    success_url = reverse_lazy('home')

    def get_queryset(self):
        query = Blog.objects.filter(author=self.request.user)
        return query


class BlogTopicListView(ListView):
    model = Blog
    template_name = 'content/topic_list.html'

    def get_queryset(self):
        qs = Blog.objects.all()
        return qs

#
# class AuthorCreateView(CreateView):
#     model = Author
#     fields = ['user','bio']
#     template_name = 'content/blog_form.html'
