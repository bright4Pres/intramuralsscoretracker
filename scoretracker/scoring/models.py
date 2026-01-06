from django.db import models
from django.utils import timezone

class Team(models.Model):
    """Model representing a team in the intramural competition."""
    TEAM_CHOICES = [
        ('shinobi', 'Shinobi'),
        ('pegasus', 'Pegasus'),
        ('chimera', 'Chimera'),
        ('phoenix', 'Phoenix'),
    ]
    
    name = models.CharField(max_length=20, choices=TEAM_CHOICES, unique=True)
    points = models.IntegerField(default=0)
    color = models.CharField(max_length=7, default='#FFFFFF')
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return f"{self.get_name_display()} - {self.points} points"


class ScoreLog(models.Model):
    """Model to track scoring history."""
    team = models.CharField(max_length=20, choices=Team.TEAM_CHOICES)
    points = models.IntegerField()
    opponent = models.CharField(max_length=100, blank=True, null=True)  # Text field - can be team name or "All"
    event = models.CharField(max_length=100)  # Free text for any event name
    team_score = models.IntegerField(default=0)  # Winner's score in the event
    opponent_score = models.IntegerField(default=0, blank=True, null=True)  # Opponent's score (if applicable)
    reason = models.TextField(blank=True, null=True)  # Reason for deduction/disqualification
    timestamp = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        opponent_text = f"vs {self.opponent}" if self.opponent else "vs All"
        return f"{self.get_team_display()} scored {self.points} pts in {self.event} {opponent_text}"
