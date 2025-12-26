# File: mini_insta/models.py
# model construction
# Author: Nguyen Le



from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    '''Encapsulate the data of a profile on instagram'''

    # attributes of a profile
    username = models.TextField(blank=True)
    display_name = models.TextField(blank=True)
    profile_image_url = models.URLField(blank=True)
    bio_text = models.TextField(blank=True)
    join_date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # method for string representation of this model
    def __str__(self):
        '''return a string representation of this model instance'''
        return f'{self.username} a.k.a. {self.display_name}'
    
    # accessor methods to retrieve related model data
    def get_all_posts(self):
        '''Return a QuerySet of Posts for a given Profile'''
        posts = Post.objects.filter(profile=self)
        return posts
    
    # redirect URL after Profile update
    def get_absolute_url(self):
        '''Return a URL to display instance of this object after updating the Profile'''
        return reverse('show_profile', kwargs={'pk': self.pk}) # generate URL to display
    
    # getter method: followers of this Profile
    def get_followers(self):
        '''Return a list of Profiles who are followers of this Profile'''
        follows = Follow.objects.filter(profile=self) # QuerySet of Follow relationships, where self is the profile being followed
        followers = [follow.follower_profile for follow in follows] # list of followers, follower_profile is the follower
        return followers
    
    def get_num_followers(self):
        '''Return the count of followers of this Profile'''
        return Follow.objects.filter(profile=self).count()
    
    # getter method: Profiles followed by this Profile
    def get_following(self):
        '''Return a list of Profiles followed by this profile'''
        follows = Follow.objects.filter(follower_profile=self) # QuerySet of Follow relationships, where self is the follower
        following = [follow.profile for follow in follows] # list of profiles self is following
        return following
    
    def get_num_following(self):
        '''Return the count of how many Profiles this Profile is following'''
        return Follow.objects.filter(follower_profile=self).count()
    
    # a Profile's post feed
    def get_post_feed(self):
        '''Return a list (or QuerySet) of Posts, for the profiles being followed by the profiles on which the method was called'''
        following_profiles = self.get_following() # get Profiles this user is following
        return Post.objects.filter(profile__in=following_profiles).order_by('-timestamp') # recent posts first
    
    
    

# Post, something you write on a Profile, there can be many posts in a profile
class Post(models.Model):
    '''Encapsulate the idea of a Post on a Profile'''

    # attributes of a post
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE) # unique identifier to Profile model
    timestamp = models.DateTimeField(auto_now=True)
    caption = models.TextField(blank=False)

    # string representation of this model
    def __str__(self):
        '''return a string representation of this model instance'''
        return f'{self.caption}'
    
    # retrieve all photos of a Post
    def get_all_photos(self):
        '''Return a QuerySet of Photos for a given Post'''
        photos = Photo.objects.filter(post=self)
        return photos
    
    # method to display url
    def get_absolute_url(self):
        '''Return a URL to display one instance of this object'''
        return reverse('show_post', kwargs={'pk': self.pk}) # generate URL to display
    
    # accessor method to get all the comments
    def get_all_comments(self):
        '''Return all the Comments related to this Post'''
        return Comment.objects.filter(post=self).order_by('-timestamp') # order the comments by recentness
    
    # accessor method to get likes of a Post
    def get_likes(self):
        '''Return all the Likes related to this Post'''
        return Profile.objects.filter(like__post=self).distinct()
    
    # method to get number of likes
    def get_num_likes(self):
        '''Return the number of Likes of a Post'''
        return self.get_likes().count()

    # Liked by XYZ and 5 others, this method will return 'XYZ'
    def get_most_recent_like(self):
        '''Return the Profile of the most recent Like'''
        likes = Like.objects.filter(post=self).order_by('-timestamp') # likes for this post, ordered by newest first
        if likes.exists():
            # first like
            return likes.first()
        else:
            # no likes yet
            return None
    
# Photo, something you include in a Post, there can be many Photos in a Post
class Photo(models.Model):
    '''Encapsulate the idea of a Photo on a Post'''

    # attributes of a photo
    post = models.ForeignKey(Post, on_delete=models.CASCADE) # unique identifier to a Post
    image_url = models.URLField(blank=True) # legacy way of getting images
    timestamp = models.DateTimeField(auto_now=True)
    image_file = models.ImageField(blank=True) # new way of getting images

    # string representation of this model
    def __str__(self):
        '''return a string representation of this model instance'''
        # image via URL
        if self.image_url:
            return f'Image used in "{self.post}" as a URL to an image'
        
        # uploaded image file
        else:
            return f'Image used in "{self.post}" as an actual uploaded image file'
    
    # accessor method
    def get_image_url(self):
        '''accessor method to return either URL stored in image_url or URL to image_file.url'''
        # image via URL
        if self.image_url:
            return self.image_url
        
        # uploaded image file 
        else:
            return self.image_file.url

# Follow, connection between two nodes 
class Follow(models.Model):
    '''Encapsulate connection when one Profile follows another Profile'''

    # attributes of Follow relationship
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="profile")
    follower_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="follower_profile")
    timestamp = models.DateTimeField(auto_now=True)

    # string representation of this model
    def __str__(self):
        '''return a string representation of this model instance'''
        return f'{self.follower_profile} follows {self.profile}'
    
# Comment, connection between Profile and Post
class Comment(models.Model):
    '''Encapsulate a Profile providing a response or commentary on a Post'''

    # attributes of Comment object
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)
    text = models.TextField(blank=False)

    # string representation of this model
    def __str__(self):
        return f'Comment by {self.profile.username} on {self.post.caption}'
    
# model for Likes of a Post
class Like(models.Model):
    '''Encapsulate a Profile providing approval of a Post'''

    # attributes of Like object
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)

    # string representation of this model
    def __str__(self):
        return f'{self.profile.username} liked the post: {self.post}'
    
# give User a .profile property 
User.add_to_class('profile',
    lambda self: Profile.objects.get(user=self)
)