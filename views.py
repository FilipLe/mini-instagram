# File: mini_insta/views.py
# views
# Author: Nguyen Le



from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse
from .forms import CreatePostForm, UpdateProfileForm, UpdatePostForm, CreateProfileForm, CreateCommentForm
from .models import Profile, Post, Photo, Follow, Like, Comment

from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Create your views here.


# custom LoginRequiredMixin
class MyLoginRequiredMixin(LoginRequiredMixin):
    '''Define a custom subclass LoginRequiredMixin as helper to force login for certain views'''

    def get_login_url(self):
        '''return the URL for this app's login page when unauthenticated'''
        # get current URL that the user was trying to access
        current_url = self.request.get_full_path()
        login_url = reverse('login')
        
        # add current URL as the 'next' parameter
        return f"{login_url}?next={current_url}"
    
    def get_logged_in_profile(self):
        '''return the Profile of logged in user'''
        user = self.request.user
        return Profile.objects.get(user=user)


'''
views without authentication
'''

# inherits ListView, which display many models
class ProfileListView(ListView):
    '''Define a view class to show all Profiles'''
    model = Profile
    template_name = "mini_insta/show_all_profiles.html"
    context_object_name = "profiles" # plural

# inherits DetailView, which displays one model
class ProfileDetailView(DetailView):
    '''Define a view class to show a single profile'''
    model = Profile
    template_name = "mini_insta/show_profile.html"
    content_object_name = "profile" # singular

class PostDetailView(DetailView):
    '''Define a view class to show a single post'''
    model = Post
    template_name = "mini_insta/show_post.html"
    context_object_name = "post" # singular

class ShowFollowersDetailView(DetailView):
    '''View class to display all followers of a Profile'''

    model = Profile
    template_name = "mini_insta/show_followers.html"
    context_object_name = "profile"

class ShowFollowingDetailView(DetailView):
    '''View class to display all Profiles that this Profile is following'''

    model = Profile
    template_name = "mini_insta/show_following.html"
    context_object_name = "profile"

class CreateProfileView(CreateView):
    '''View class to handle the creation of a new Profile/User'''

    template_name = 'mini_insta/create_profile_form.html'
    form_class = CreateProfileForm

    def get_success_url(self):
        '''Provide a URL to redirect to after creating a new User Profile'''
        return reverse('show_all_profiles')
    
    def get_context_data(self, **kwargs):
        '''Context variables for creating User form'''
        context = super().get_context_data(**kwargs)
        context['user_form'] = UserCreationForm()
        return context

    def form_valid(self, form):
        '''Reconstruct UserCreationForm from POST data'''
        user_form = UserCreationForm(self.request.POST)

        if user_form.is_valid():
            # save new User
            user = user_form.save()

            # attach user to Profile
            form.instance.user = user
            
            # auto log in
            login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')

            # save the Profile
            return super().form_valid(form)
       
        else:
            context = self.get_context_data()
            context['user_form'] = user_form
            return self.render_to_response(context)

'''
authenticated views - CRUD
'''

class CreatePostView(MyLoginRequiredMixin, CreateView):
    '''A view to handle the creation of a new Post on a Profile'''

    form_class = CreatePostForm
    template_name = "mini_insta/create_post_form.html"

    # url that redirects user after user submits a new comment successfully
    def get_success_url(self):
        '''Provide a URL to redirect to after creating a new Comment'''
        
        # use reverse function to create and return a URL
        return reverse('show_post', kwargs={'pk' : self.object.pk})
    
    # context data
    def get_context_data(self):
        '''Return the dictionary of context variables for use in the template'''

        # calling the superclass method
        context = super().get_context_data()

        # find/add the profile to the context data
        # retrieve the PK from the URL pattern
        # pk = self.kwargs['pk']
        # profile = Profile.objects.get(pk=pk)

        # add this profile into the context dictionary
        # context['profile'] = profile

        # provide profile (the logged-in user's profile) to the template
        profile = self.get_logged_in_profile()
        context['profile'] = profile
        return context
    
    # override form_valid method which handles creating new comment object into database
    def form_valid(self, form):
        '''This method handles the form submission and saves the 
        new object to the Django database.
        We need to add the foreign key (of the Profile) to the Post
        object before saving it to the database.
        '''

        print(form.cleaned_data)

        # retrieve the PK from the URL pattern
        # pk = self.kwargs['pk']
        # profile = Profile.objects.get(pk=pk)

        # attach the logged-in profile as the post owner
        profile = self.get_logged_in_profile()

        # attach this profile to the post
        form.instance.profile = profile 

        # delegate the work to the superclass method form_valid and save instance
        response = super().form_valid(form) 

        # legacy system: create a Photo for this post using URL of image
        # image_url = self.request.POST.get("image_url")
        # if image_url:
        #     Photo.objects.create(post=self.object, image_url=image_url)

        # create and save Photo objects for this post, from multiple uploaded files
        files = self.request.FILES.getlist('files')

        # if there is image file
        if files:
            for file in files:
                Photo.objects.create(post=self.object, image_file = file)
        # otherwise just save "no image found" file
        else:
            Photo.objects.create(post=self.object, image_file="default.png")

        return response
    
class UpdateProfileView(MyLoginRequiredMixin, UpdateView):
    '''View class to handle update to an Profile based on its PK'''

    model = Profile
    form_class = UpdateProfileForm
    template_name = "mini_insta/update_profile_form.html"

    def get_object(self):
        '''return the Profile corresponding to the logged in user'''
        return self.get_logged_in_profile()


class DeletePostView(MyLoginRequiredMixin, DeleteView):
    '''View class to delete a Post on a Profile'''

    model = Post
    template_name = "mini_insta/delete_post_form.html"

    # override get_context_data
    def get_context_data(self, **kwargs):
        '''return the dictionary of context variables for use in the template'''
        # calling the superclass method
        context = super().get_context_data(**kwargs)

        # find the pk for this Post
        pk = self.kwargs['pk']

        # find the Post object
        post = Post.objects.get(pk=pk)

        # find the PK of the Profile to which this Post is associated
        profile = post.profile

        # add these into context dictionary
        context['post'] = post
        context['profile'] = profile

        return context

    # override get_success_url
    def get_success_url(self):
        '''return the URL to redirect to after a successful delete'''

        # find the pk for this Post
        pk = self.kwargs['pk']

        # find the Post object
        post = Post.objects.get(pk=pk)

        # find the PK of the Profile to which this Post is associated
        profile = post.profile

        return reverse('show_profile', kwargs={'pk': profile.pk})
    

class UpdatePostView(MyLoginRequiredMixin, UpdateView):
    '''View class to update a Post'''

    model = Post
    form_class = UpdatePostForm
    template_name = "mini_insta/update_post_form.html"

    def get_success_url(self):
        '''return the URL to redirect to after successful update'''

        # find the pk for this Post
        pk = self.kwargs['pk']

        # find the Post object
        post = Post.objects.get(pk=pk) 

        # return the URL to redirect to, which is the URL of the post
        return reverse('show_post', kwargs={'pk': post.pk})

class CreateCommentView(MyLoginRequiredMixin, CreateView):
    '''View class to create a Comment'''
    model = Comment
    form_class = CreateCommentForm
    template_name = 'mini_insta/create_comment_form.html'

    # override get_context_data
    def get_context_data(self, **kwargs):
        '''context variable for use to create comment'''
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        context['post'] = Post.objects.get(pk=pk)
        return context

    # override form_valid which handles saving objects to database
    def form_valid(self, form):
        '''saving post and profile to this Comment'''
        pk = self.kwargs['pk']
        post = Post.objects.get(pk=pk)

        form.instance.post = post
        form.instance.profile = self.get_logged_in_profile()
        
        return super().form_valid(form)

    def get_success_url(self):
        '''url to redirect to after successfully submitting a Comment'''
        return reverse('show_post', kwargs={'pk': self.kwargs['pk']})

# inherits DetailView, which displays one model
class LoggedInProfileDetailView(MyLoginRequiredMixin, DetailView):
    '''View class to show the profile of the logged in user specifically'''
    model = Profile
    template_name = "mini_insta/show_profile.html"
    content_object_name = "profile" # singular

    def get_object(self):
        '''return the logged-in user's profile'''
        return self.get_logged_in_profile()

class PostFeedListView(MyLoginRequiredMixin, ListView):
    '''View class to display the Post Feed of a Profile, showing Posts from profiles the user follows'''

    model = Post
    template_name = "mini_insta/show_feed.html"
    context_object_name = "posts" # plural

    def get_queryset(self):
        '''retrieve posts from all profiles the current profile is following'''
        # find the pk for this Post
        # pk = self.kwargs['pk']  

        # # find the Profile object
        # profile = Profile.objects.get(pk=pk)

        profile = self.get_logged_in_profile()

        # return the Post feed related to this Profile
        return profile.get_post_feed()

    def get_context_data(self, **kwargs):
        '''return the dictionary of context variables for use in the template'''
        # calling the superclass method
        context = super().get_context_data(**kwargs)

        # find the pk for this Post
        # pk = self.kwargs['pk']

        # add the Profile to the context for template usage.
        # context['profile'] = Profile.objects.get(pk=pk)

        context['profile'] = self.get_logged_in_profile()

        return context

class SearchView(MyLoginRequiredMixin, ListView):
    '''View class to display the search of a Profile or a Post'''

    template_name = "mini_insta/search_results.html"
    context_object_name = "posts"

    def dispatch(self, request, *args, **kwargs):
        '''dispatch (handle) any request'''
        # get the query string from the GET parameters
        self.query = request.GET.get('query', '').strip() 

        # find the pk
        # pk = self.kwargs['pk']

        # get the profile for whom the search is being done
        # self.profile = Profile.objects.get(pk=pk)
        self.profile = self.get_logged_in_profile()

        # If no query yet, render the search form page
        if not self.query:
            return render(request, "mini_insta/search.html", {"profile": self.profile})

        # there is query
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        '''Return QuerySet of Posts that match the search query'''
        return Post.objects.filter(caption__contains=self.query).order_by('-timestamp') # most recent first
    
    def get_context_data(self, **kwargs):
        '''Return the context dictionary for template rendering'''
        # calling the superclass method
        context = super().get_context_data(**kwargs)

        # add the Profile that the query is done on behalf of, profile with PK
        context['profile'] = self.profile

        # add the Query to the context
        context['query'] = self.query

        # add the Posts that match the query to context
        context['posts'] = self.get_queryset()

        # matching profiles with username, name, or text that match the query
        context['profiles'] = (
            Profile.objects.filter(username__contains=self.query) | Profile.objects.filter(display_name__contains=self.query) | Profile.objects.filter(bio_text__contains=self.query)
        )

        return context
    

class LogoutConfirmationView(TemplateView):
    '''View class to display logout confirmation page'''
    
    template_name="mini_insta/logged_out.html"



class FollowView(MyLoginRequiredMixin, TemplateView):
    '''View class to handle the action of Following an account'''
    def dispatch(self, request, *args, **kwargs):
        '''dispatch (handle) the request to follow an account'''
        # retrieve the Profile requesting to follow and the Profile to be followed
        profile_to_follow = Profile.objects.get(pk=kwargs['pk'])
        follower = self.get_logged_in_profile()

        # if they are not the same profiles, allow the action
        if profile_to_follow != follower:
            Follow.objects.get_or_create(
                profile=profile_to_follow,
                follower_profile=follower
            )
        return redirect('show_profile', pk=kwargs['pk'])


class UnfollowView(MyLoginRequiredMixin, TemplateView):
    '''View class to handle the action of Unollowing an account'''
    def dispatch(self, request, *args, **kwargs):
        '''dispatch (handle) the request to unfollow an account'''
        profile_to_unfollow = Profile.objects.get(pk=kwargs['pk'])
        follower = self.get_logged_in_profile()

        # filter through Profiles and when they are found in the Follow relationship, delete that
        Follow.objects.filter(
            profile=profile_to_unfollow,
            follower_profile=follower
        ).delete()
        return redirect('show_profile', pk=kwargs['pk'])


class LikeView(MyLoginRequiredMixin, TemplateView):
    '''View class to handle the action of Liking a Post'''
    def dispatch(self, request, *args, **kwargs):
        '''dispatch (handle) the request to like a Post'''
        post = Post.objects.get(pk=kwargs['pk'])
        liker = self.get_logged_in_profile()

        # make sure the Profile is not liking their own Post
        if post.profile != liker:
            Like.objects.get_or_create(post=post, profile=liker)
        return redirect('show_post', pk=kwargs['pk'])


class UnlikeView(MyLoginRequiredMixin, TemplateView):
    '''View class to handle the action of Unliking a Post'''
    def dispatch(self, request, *args, **kwargs):
        '''dispatch (handle) the request to unlike a Post'''
        post = Post.objects.get(pk=kwargs['pk'])
        liker = self.get_logged_in_profile()

        # Delete the Like relationship if the profile matches the liker of the Post
        Like.objects.filter(post=post, profile=liker).delete()
        return redirect('show_post', pk=kwargs['pk'])