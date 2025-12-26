# File: mini_insta/urls.py
# url patterns
# Author: Nguyen Le


from django.urls import path
from .views import * 
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', ProfileListView.as_view(), name="show_all_profiles"), # display all profiles on the app
    path('profile/<int:pk>', ProfileDetailView.as_view(), name="show_profile"), # display specific profile
    path('post/<int:pk>', PostDetailView.as_view(), name="show_post"), # display specific post

    # authenticated user specific - no pk
    path('profile/create_post', CreatePostView.as_view(), name="create_post"), # create a post 
    path('profile/update', UpdateProfileView.as_view(), name='update_profile'), # update a profile 
    path('profile/feed', PostFeedListView.as_view(), name="show_feed"), # display post feed of a profile
    path('profile/search', SearchView.as_view(), name='search'), # search function
    path('profile/', LoggedInProfileDetailView.as_view(), name='profile'), # new requirement: display logged in user profile

    # post specific - keep pk of the post, not pk of user
    path('post/<int:pk>/delete', DeletePostView.as_view(), name="delete_post"), # delete a post 
    path('post/<int:pk>/update', UpdatePostView.as_view(), name="update_post"), # update a post 
    path('post/<int:pk>/comment', CreateCommentView.as_view(), name='add_comment'), # add comment to post

    # action specific
    path('profile/<int:pk>/follow', FollowView.as_view(), name='follow'), # follow profile
    path('profile/<int:pk>/delete_follow', UnfollowView.as_view(), name='unfollow'), # unfollow profile
    path('post/<int:pk>/like', LikeView.as_view(), name='like'), # like post
    path('post/<int:pk>/delete_like', UnlikeView.as_view(), name='unlike'), # unlike post

    # public
    path('profile/<int:pk>/followers', ShowFollowersDetailView.as_view(), name='show_followers'), # show followers
    path('profile/<int:pk>/following', ShowFollowingDetailView.as_view(), name='show_following'), # show profiles following

    # authentication related url 
    path('login/', auth_views.LoginView.as_view(template_name="mini_insta/login.html"), name="login"), # login screen
    path('logout_confirmation/', LogoutConfirmationView.as_view(), name="logout_confirmation"), # logout confirmation 
    path('logout/', auth_views.LogoutView.as_view(next_page='logout_confirmation'), name="logout"), # logout function
    path('create_profile/', CreateProfileView.as_view(), name='create_profile'), # creating new User Profile function
]