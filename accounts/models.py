from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
import post.models
from django.utils.translation import gettext as _

class User(AbstractUser):
    user_id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        primary_key=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    liked_tags = models.ManyToManyField('post.Tag' , blank=True, related_name='user_liked')
    disliked_tags = models.ManyToManyField('post.Tag', blank=True, related_name='user_disliked')
    
    