from django.db import models

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
