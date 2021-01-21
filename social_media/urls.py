from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from post.views import home

urlpatterns = [
    path('', include('rest_auth.urls')),
    path('registration/', include('rest_auth.registration.urls')),
    path('api/', include('post.urls')),
    path('admin/', admin.site.urls),
    path('',home),
]
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)