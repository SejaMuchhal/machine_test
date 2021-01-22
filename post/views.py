from django.shortcuts import render, get_object_or_404
from rest_framework import generics
from rest_framework import status
from .models import Post, Tag
from rest_framework.response import Response
from .serializers import GetUserIDSerializer, PostSerializer, PostReactionSerializer, GetPostIDSerializer, UserSerializer
from rest_framework.generics import DestroyAPIView, UpdateAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework import serializers
from .pagination import CustomPagination
from rest_framework.exceptions import NotFound
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from social_media import settings
from django.db.models import Max

User = settings.AUTH_USER_MODEL

@api_view(('GET',))
def home(request):
    return Response({"message":"Welcome Home!"},
                    status=status.HTTP_200_OK)

class PostListView(generics.ListCreateAPIView): 
    serializer_class = GetUserIDSerializer
    serializer_class_post = PostSerializer
    permission_classes = [IsAuthenticated]
    queryset = ''
    context_object_name = "post_list"

    def get_queryset_Post(self, user):
        liked_posts = Post.objects.filter(tags__in=user.liked_tags.all()).annotate(max_weight=Max('tags__weight')).order_by('-max_weight')
        normal_posts = Post.objects.exclude(tags__in=user.liked_tags.all()).exclude(tags__in=user.disliked_tags.all()).annotate(max_weight=Max('tags__weight'))
        disliked_posts = Post.objects.filter(tags__in=user.disliked_tags.all()).annotate(max_weight=Max('tags__weight')).order_by('max_weight')
        sorted_posts = liked_posts | normal_posts | disliked_posts
        return sorted_posts

    def post(self, request):
        user = request.user
        page = self.request.data.get('page')
        queryset = self.get_queryset_Post(user)
        paginator = CustomPagination()
        p = paginator.paginate_queryset(queryset=queryset, request=request)
        serializer = self.serializer_class_post(
            p,
            many=True,
            context={'user': user}
            )
        return paginator.get_paginated_response(serializer.data)

class PostReactionView(generics.ListCreateAPIView):
    serializer_class = PostReactionSerializer
    permission_classes = [IsAuthenticated]
    queryset = ''
    context_object_name = "like_dislike_post"

    def post(self, request, *args, **kwargs):
        post_id = self.request.data.get('post_id')
        reaction = int(self.request.data.get('reaction'))
        post = get_object_or_404(Post, post_id=post_id)
        user = request.user 
        tags = Tag.objects.filter(post=post)
        if reaction==1:
            post.liked_users.add(user)
            user.liked_tags.add(*tags)
            post.disliked_users.remove(user)
            user.disliked_tags.remove(*tags)
            response = True
            message = 'Post liked successfully'
        elif reaction==2:
            post.disliked_users.add(user)
            user.disliked_tags.add(*tags)
            post.liked_users.remove(user)
            user.liked_tags.remove(*tags)
            response = True
            message = 'Post disliked successfully'
        else:
            return Response({"status": False, "message": "Invalid request."}, status=status.HTTP_400_BAD_REQUEST)
        return Response (
            {
                "status_code": status.HTTP_200_OK,
                "status": response,
                "message":message,
                }
        )
        
class LikedUsersList(generics.ListCreateAPIView):    
    serializer_class = GetPostIDSerializer
    serializer_class_user = UserSerializer
    permission_classes = [IsAuthenticated]
    queryset = ''
    context_object_name = "users_list"
    
    def get_queryset_User(self, post_id):
        post = get_object_or_404(Post, post_id=post_id)
        return User.objects.filter()
        
    def post(self, request):
        post_id = self.request.data.get('post_id')
        post = get_object_or_404(Post, post_id=post_id)
        queryset = self.get_queryset_User(post_id)
        paginator = CustomPagination()
        paginator.page_size = 5
        p = paginator.paginate_queryset(queryset=queryset, request=request) 
        serializer = self.serializer_class_user(
            p,
            many=True,
            ) 
        return paginator.get_paginated_response(serializer.data)
