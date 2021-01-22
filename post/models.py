from django.db import models
import uuid
from django.utils.translation import gettext as _
from social_media import settings

User = settings.AUTH_USER_MODEL

class Post(models.Model):
    description = models.TextField()
    post_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_on = models.DateField(auto_now_add=True, verbose_name=_("created on"))
    liked_users = models.ManyToManyField(User, blank=True, related_name='liked_post')
    disliked_users = models.ManyToManyField(User, blank=True, related_name='disliked_post')

    def like_count(self):
        no_of_likes = self.liked_users.all().count()
        return no_of_likes
    
    def dislike_count(self):
        no_of_dislikes = self.disliked_users.all().count()
        return no_of_dislikes
          
    def __str__(self):
        if len(self.description) >10:
            name = self.description[0:10]
        else:
            name = self.description
        return name
   
class Image(models.Model):
    post = models.ForeignKey(Post, null=True, default=None, on_delete=models.CASCADE, related_name='images')
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    images = models.ImageField(upload_to = 'images/')

    def get_image_url(self):
        return self.images.url
    def __str__(self):
        return self.images.url


class Tag(models.Model):
    name = models.CharField(max_length=100)
    weight = models.IntegerField(default=0)
    post = models.ManyToManyField(Post, related_name='tags')
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        return ' Name- ' + self.name + ', Weight- ' + str(self.weight)
        