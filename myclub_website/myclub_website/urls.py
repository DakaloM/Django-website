
from django.contrib import admin
from django.urls import path, include
from django.conf import settings                    
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('events.urls')),
    path('members/',include('django.contrib.auth.urls')), #allow us to use django user authentications
    path('members/',include('members.urls')),
]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)


# Configure Admin Titles

admin.site.site_header = "My Club Adminitrator Area"
admin.site.site_title = "Browser title"
admin.site.index_title = "Welcome to the admin area"