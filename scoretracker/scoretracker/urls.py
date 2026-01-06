"""
URL configuration for scoretracker project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from scoring import views

urlpatterns = [
    path('', views.home, name='home'),
    path('logs/', views.logs, name='logs'),
    path('admin-login/', views.admin_login, name='admin_login'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-logout/', views.admin_logout, name='admin_logout'),
    path('api/scores/', views.get_scores, name='get_scores'),
    path('api/logs/', views.get_logs, name='get_logs'),
    path('api/add-points/', views.add_points, name='add_points'),
    path('api/reset-scores/', views.reset_scores, name='reset_scores'),
    path('admin/', admin.site.urls),
]
