from django.contrib import admin
from .models import Blog, Vote, Comment

admin.site.register([Blog, Vote, Comment])
