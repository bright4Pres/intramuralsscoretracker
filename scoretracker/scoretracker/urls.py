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
from django.conf import settings
from django.conf.urls.static import static
from scoring import views

urlpatterns = [
    path('', views.home, name='home'),
    path('health/', views.health_check, name='health_check'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('logs/', views.logs, name='logs'),
    path('admin-login/', views.admin_login, name='admin_login'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-logout/', views.admin_logout, name='admin_logout'),
    path('api/scores/', views.get_scores, name='get_scores'),
    path('api/logs/', views.get_logs, name='get_logs'),
    path('api/add-points/', views.add_points, name='add_points'),
    path('api/add-game-result/', views.add_game_result, name='add_game_result'),
    path('api/reset-scores/', views.reset_scores, name='reset_scores'),
    path('api/game-results/', views.get_game_results, name='get_game_results'),
    path('api/set-game-result/', views.set_game_result, name='set_game_result'),
    path('api/add-special-award/', views.add_special_award, name='add_special_award'),
    path('api/special-awards/<int:game_id>/', views.get_special_awards, name='get_special_awards'),
    path('api/delete-special-award/<int:award_id>/', views.delete_special_award, name='delete_special_award'),
    path('api/clear-special-award/<int:award_id>/', views.delete_special_award, name='clear_special_award'),
    path('admin/', admin.site.urls),
    path('mrmspisay/', views.mrmspisay_showcase, name='mrmspisay_showcase'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
