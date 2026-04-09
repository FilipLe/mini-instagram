# File: mini_insta/admin.py
# model registration
# Author: Nguyen Le


from django.contrib import admin

# Register your models here.
from .models import Profile, Post, Photo, Follow, Comment, Like

admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Photo)
admin.site.register(Follow)
admin.site.register(Comment)
admin.site.register(Like)