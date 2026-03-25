from django.contrib import admin
from django.urls import path

from dashboard import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('api/live/', views.live_data, name='live_data'),
]
