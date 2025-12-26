# File: mini_insta/forms.py
# define the forms that we use for create/update/delete operations
# Author: Nguyen Le

from django import forms
from .models import *

class CreatePostForm(forms.ModelForm):
    '''A form to add a Post to the database'''

    class Meta:
        '''associate this form with Post model from our database'''
        model = Post
        fields = ['caption']

class UpdateProfileForm(forms.ModelForm):
    '''A form to update a Profile in the database'''

    class Meta:
        '''associate this form with Profile model from our database'''
        model = Profile
        fields = ['display_name', 'bio_text', 'profile_image_url'] # fields can be updated in a profile

class UpdatePostForm(forms.ModelForm):
    '''A form to update a Post in the database'''

    class Meta:
        '''associate this form with Post model from our database'''
        model = Post
        fields = ['caption'] # allowed to update text

class CreateProfileForm(forms.ModelForm):
    '''A form to create Profile'''

    class Meta:
        '''associate this form with Profile model'''
        model = Profile
        fields = ['username', 'display_name', 'bio_text', 'profile_image_url']

class CreateCommentForm(forms.ModelForm):
    '''Form to create a new Comment on a Post'''
    
    class Meta:
        model = Comment
        fields = ['text']