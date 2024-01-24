from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('main/', include('GenesysAuthenticator.urls')),
    path('', include('GenesysUserApp.urls')),
]
