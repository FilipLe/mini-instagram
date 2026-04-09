from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Photo, Post, Profile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name"]


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    num_followers = serializers.SerializerMethodField()
    num_following = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = [
            "id",
            "username",
            "display_name",
            "profile_image_url",
            "bio_text",
            "join_date",
            "user",
            "num_followers",
            "num_following",
        ]

    def get_num_followers(self, obj):
        return obj.get_num_followers()

    def get_num_following(self, obj):
        return obj.get_num_following()


class PhotoSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Photo
        fields = ["id", "image", "timestamp"]

    def get_image(self, obj):
        request = self.context.get("request")
        image_url = obj.get_image_url()
        if request is not None and image_url and image_url.startswith("/"):
            return request.build_absolute_uri(image_url)
        return image_url


class PostSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    photos = PhotoSerializer(many=True, read_only=True, source="photo_set")
    num_likes = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ["id", "profile", "timestamp", "caption", "photos", "num_likes"]

    def get_num_likes(self, obj):
        return obj.get_num_likes()

