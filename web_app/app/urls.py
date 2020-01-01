from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('api/v1/socnet/', include('socnet.urls')),
    path('admin/', admin.site.urls),
]
