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
        
    def get_liked_users(self):
        return ", ".join([u.username for u in self.liked_users.all()])

    def like_count(self):
        no_of_likes = self.liked_users.all().count()
        return no_of_likes
    
    def dislike_count(self):
        no_of_dislikes = self.disliked_users.all().count()
        return no_of_dislikes
        
    def get_tag_weight(self):
        tag_set = Tag.objects.filter(post=self)
        tag_weight = 0
        for tag in tag_set:
            tag_weight += tag.weight
        return tag_weight
          

    def __str__(self):
        if len(self.description) >10:
            name = self.description[0:10]
        else:
            name = self.description
        return name
   
class Image(models.Model):
    post = models.ForeignKey(Post, null=True, default=None, on_delete=models.CASCADE, related_name='parent_post')
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    images = models.ImageField(upload_to = 'images/')
    
    def __str__(self):
        return self.images.url

    def get_image_url(self):
        return self.images.url

class Tag(models.Model):
    name = models.CharField(max_length=100)
    weight = models.IntegerField(default=0)
    post = models.ForeignKey(Post, null=True, default=None, on_delete=models.CASCADE, related_name='post')
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        return ' Name- ' + self.name + ', Weight- ' + str(self.weight)