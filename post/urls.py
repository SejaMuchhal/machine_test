from django.urls import include, path
from . import views

urlpatterns = [
    
    path('get_posts', views.PostListView.as_view()),
    path('post_reaction', views.PostReactionView.as_view()),
    path('liked_userslist', views.LikedUsersList.as_view()),
]