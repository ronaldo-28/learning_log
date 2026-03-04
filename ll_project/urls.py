# ll_project/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('allauth.urls')),
    path('', include('django.contrib.auth.urls')),  # ← Add this line
    path('', include('learning_logs.urls')),
]