from django.contrib import admin
from post.models import Post, Tag, Image

class PostImageAdmin(admin.StackedInline):
    model = Image
    extra = 1

admin.site.register(Tag)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    fields = ('description',)
    list_display = ('description','like_count', 'dislike_count')
    inlines = [PostImageAdmin]
 
    class Meta:
       model = Post
 

