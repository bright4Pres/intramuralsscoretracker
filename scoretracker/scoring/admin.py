from django.contrib import admin
from .models import Team, ScoreLog, Game, GameResult


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'type', 'points_1st', 'points_2nd', 'points_3rd', 'points_4th', 'points_dq', 'is_active']
    list_filter = ['category', 'type', 'is_active']
    search_fields = ['name']
    list_editable = ['is_active']


@admin.register(GameResult)
class GameResultAdmin(admin.ModelAdmin):
    list_display = ['game', 'team', 'placement', 'timestamp']
    list_filter = ['game__type', 'game__category', 'team', 'placement']
    search_fields = ['game__name', 'team']
    readonly_fields = ['timestamp']


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['name', 'points', 'color']
    list_editable = ['points', 'color']


@admin.register(ScoreLog)
class ScoreLogAdmin(admin.ModelAdmin):
    list_display = ['team', 'event', 'points', 'opponent', 'team_score', 'opponent_score', 'timestamp']
    list_filter = ['team', 'timestamp']
    search_fields = ['event', 'opponent']
    readonly_fields = ['timestamp']
