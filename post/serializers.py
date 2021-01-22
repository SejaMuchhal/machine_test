from rest_framework import serializers
from django.shortcuts import get_object_or_404
from .models import Post, Tag, Image
from social_media import settings

User = settings.AUTH_USER_MODEL

class PostSerializer(serializers.Serializer):
    post_id = serializers.UUIDField()
    description = serializers.CharField()
    images = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    like_count = serializers.IntegerField()
    dislike_count = serializers.IntegerField()
    created_on = serializers.DateField()
    
    class Meta:
        fields = '__all__'
        read_only_fields = fields

    def get_is_liked(self, instance):
        user = self.context.get("user")
        liked_users_set = instance.liked_users.all()
        disliked_users_set = instance.disliked_users.all()
        status = None
        if user in liked_users_set:
            status = True
        elif user in disliked_users_set:
            status = False
        return status
    
    def get_images(self, instance):
        image_set = Image.objects.filter(post=instance)
        urlset = set()
        for image in image_set:
            urlset.add(image.get_image_url())       
        return urlset
   

class PostReactionSerializer(serializers.Serializer):
    reaction = serializers.IntegerField(default=0)
    post_id = serializers.UUIDField()

    class Meta:
        fields = '__all__'

class GetPostIDSerializer(serializers.Serializer):
    post_id = serializers.UUIDField()
    page = serializers.IntegerField(default=1)

    class Meta:
        fields = ('post_id','page',)
        
class UserSerializer(serializers.Serializer):
    user_id = serializers.UUIDField()
    username = serializers.CharField()
    email = serializers.EmailField()

    class Meta:
        fields = '__all__'
        read_only_fields = fields

class GetUserIDSerializer(serializers.Serializer):
    page = serializers.IntegerField(default=1)

    class Meta:
        fields = '__all__'