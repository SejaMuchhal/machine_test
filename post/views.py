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
        liked_tags = user.liked_tags.all()
        disliked_tags = user.disliked_tags.all()
        posts = Post.objects.all()
        sorted_posts = []
        liked_posts = []
        disliked_posts = []
        normal_posts = []
        for post in posts:
            is_break = False
            is_added = False
            post_tags = Tag.objects.filter(post=post)
            for tag in post_tags:
                if is_break:
                    break
                for liked_tag in liked_tags:
                    if tag.name == liked_tag.name:
                        liked_posts.append(post)
                        is_break = True
                        is_added = True
                        break
                else:
                    for disliked_tag in disliked_tags:
                        if tag.name == disliked_tag.name:
                            disliked_posts.append(post)
                            is_added = True
                            is_break = True
                            break
            if is_added == False:
                normal_posts.append(post)
                continue
        for i in range(len(liked_posts)):
            for j in range(i + 1, len(liked_posts)):
                if liked_posts[i].get_tag_weight() < liked_posts[j].get_tag_weight():
                    liked_posts[i], liked_posts[j] = liked_posts[j], liked_posts[i]
        for i in range(len(disliked_posts)):
            for j in range(i + 1, len(disliked_posts)):
                if disliked_posts[i].get_tag_weight() > disliked_posts[j].get_tag_weight():
                    disliked_posts[i], disliked_posts[j] = disliked_posts[j], disliked_posts[i]
        sorted_posts = liked_posts  + normal_posts + disliked_posts
        return sorted_posts

            
    def post(self, request):
        user = request.user
        page = self.request.data.get('page')
        queryset = self.get_queryset_Post(user)
        paginator = CustomPagination()
        p = paginator.paginate_queryset(queryset=queryset, request=request)
        if p is not None: 
            serializer = self.serializer_class_post(
                p,
                many=True,
                context={'user': user}
                )
            return paginator.get_paginated_response(serializer.data)
        return Response({"message": "No content to show.",}, status=status.HTTP_204_NO_CONTENT)

class PostReactionView(generics.ListCreateAPIView):
    serializer_class = PostReactionSerializer
    permission_classes = [IsAuthenticated]
    queryset = ''

    def post(self, request, *args, **kwargs):
        post_id = self.request.data.get('post_id')
        reaction = int(self.request.data.get('reaction'))
        post = get_object_or_404(Post, post_id=post_id)
        user = request.user 
        liked_users_set = post.liked_users.all()
        disliked_users_set = post.disliked_users.all()
        user_liked_tags = user.liked_tags.all()
        user_disliked_tags = user.disliked_tags.all()
        tags = Tag.objects.filter(post=post)
        
        if reaction==1:
            response = True
            message = 'Post liked successfully'
            if user in disliked_users_set:
                user.disliked_posts.remove(post)
                post.disliked_users.remove(user)
            elif user in liked_users_set:
                response = False
                message = 'Post already liked'
            else:
                user.liked_posts.add(post)
                post.liked_users.add(user)
            for tag in tags:
                if user_liked_tags:
                    for liked_tag in user_liked_tags:
                        if liked_tag.name != tag.name:
                            user.liked_tags.add(tag)
                else:
                    user.liked_tags.add(tag)
                if user_disliked_tags:
                    for disliked_tag in user_disliked_tags:
                        if disliked_tag.name == tag.name:
                            user.disliked_tags.remove(disliked_tag)
        elif reaction==2:
            response = True
            message = 'Post disliked successfully'
            if user in liked_users_set:
                user.liked_posts.remove(post)
                post.liked_users.remove(user)
            elif user in disliked_users_set:
                response = False
                message = 'Post already disliked'
            else:
                user.disliked_posts.add(post)
                post.disliked_users.add(user)
            for tag in tags:
                if user_disliked_tags:
                    for disliked_tag in user_disliked_tags:
                        if disliked_tag.name != tag.name:
                            user.disliked_tags.add(tag)
                else:
                    user.disliked_tags.add(tag)
                if user_liked_tags:
                    for liked_tag in user_liked_tags:
                            if liked_tag.name == tag.name:
                                user.liked_tags.remove(liked_tag)
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
    paginate_by = 10
    
    def get_queryset_User(self, post_id):
        post = get_object_or_404(Post, post_id=post_id)
        return post.liked_users.all()
        
    def post(self, request):
        post_id = self.request.data.get('post_id')
        post = get_object_or_404(Post, post_id=post_id)
        queryset = self.get_queryset_User(post_id)
        paginator = CustomPagination()
        paginator.page_size = 5
        p = paginator.paginate_queryset(queryset=queryset, request=request) 
        if p is not None:
            serializer = self.serializer_class_user(
                p,
                many=True,
                ) 
            return paginator.get_paginated_response(serializer.data)
