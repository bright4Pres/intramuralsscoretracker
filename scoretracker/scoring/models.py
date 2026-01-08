from django.db import models
from django.utils import timezone


class Game(models.Model):
    """Model representing a game/event in the competition."""
    CATEGORY_CHOICES = [
        ('major', 'Major'),
        ('minor', 'Minor'),
        ('minigame', 'Minigame'),
    ]
    
    TYPE_CHOICES = [
        ('sports', 'Sports'),
        ('litmus', 'LITMUS'),
        ('minigame', 'Minigame'),
    ]
    
    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    
    # Points for different placements
    points_1st = models.IntegerField()
    points_2nd = models.IntegerField()
    points_3rd = models.IntegerField()
    points_4th = models.IntegerField()
    points_dq = models.IntegerField()
    
    # Special notes (e.g., for Mr. and Ms. Pisay special awards)
    notes = models.TextField(blank=True, null=True)
    
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['type', 'category', 'name']
    
    def __str__(self):
        return f"{self.name} ({self.get_category_display()} - {self.get_type_display()})"


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


class GameResult(models.Model):
    """Model to track game results and placements."""
    PLACEMENT_CHOICES = [
        (1, '1st Place'),
        (2, '2nd Place'),
        (3, '3rd Place'),
        (4, '4th Place'),
        (5, 'DQ'),
    ]
    
    game = models.ForeignKey('Game', on_delete=models.CASCADE, related_name='results')
    team = models.CharField(max_length=20, choices=Team.TEAM_CHOICES)
    placement = models.IntegerField(choices=PLACEMENT_CHOICES)
    notes = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['game', 'placement']
        unique_together = ['game', 'team']  # Each team can only have one placement per game
    
    def __str__(self):
        return f"{self.get_team_display()} - {self.get_placement_display()} in {self.game.name}"
    
    def save(self, *args, **kwargs):
        """Auto-calculate points when saving based on placement."""
        is_new = self.pk is None
        super().save(*args, **kwargs)
        
        # Calculate points based on placement
        points_map = {
            1: self.game.points_1st,
            2: self.game.points_2nd,
            3: self.game.points_3rd,
            4: self.game.points_4th,
            5: self.game.points_dq,
        }
        points = points_map.get(self.placement, 0)
        
        # Update team points if this is a new result
        if is_new and points != 0:
            team = Team.objects.get(name=self.team)
            team.points += points
            team.save()
            
            # Create score log
            ScoreLog.objects.create(
                team=self.team,
                points=points,
                event=self.game.name,
                opponent='All',
                team_score=self.placement,
                reason=f"Placement: {self.get_placement_display()}"
            )
    
    def delete(self, *args, **kwargs):
        """Refund points when deleting a game result."""
        # Calculate points to refund based on placement
        points_map = {
            1: self.game.points_1st,
            2: self.game.points_2nd,
            3: self.game.points_3rd,
            4: self.game.points_4th,
            5: self.game.points_dq,
        }
        points = points_map.get(self.placement, 0)
        
        # Refund team points
        if points != 0:
            team = Team.objects.get(name=self.team)
            team.points -= points
            team.save()
            
            # Create score log for refund
            ScoreLog.objects.create(
                team=self.team,
                points=-points,
                event=self.game.name,
                opponent='All',
                team_score=self.placement,
                reason=f"Refund: {self.get_placement_display()} cleared"
            )
        
        super().delete(*args, **kwargs)


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


class SpecialAward(models.Model):
    """Model to track special awards for Mr. and Miss Pisay events."""
    game = models.ForeignKey('Game', on_delete=models.CASCADE, related_name='special_awards')
    award_name = models.CharField(max_length=100)  # e.g., "Best in Evening Gown", "People's Choice"
    team = models.CharField(max_length=20, choices=Team.TEAM_CHOICES, blank=True, null=True)
    points = models.IntegerField(default=5)
    timestamp = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['game', 'award_name']
        unique_together = ['game', 'award_name']  # Each award name must be unique per game
    
    def __str__(self):
        team_name = dict(Team.TEAM_CHOICES).get(self.team, 'TBD') if self.team else 'TBD'
        return f"{self.game.name} - {self.award_name}: {team_name}"
    
    def save(self, *args, **kwargs):
        """Auto-update team points when awarding."""
        is_new = self.pk is None
        old_team = None
        
        # Check if this is an update and get the old team
        if not is_new:
            try:
                old_award = SpecialAward.objects.get(pk=self.pk)
                old_team = old_award.team
            except SpecialAward.DoesNotExist:
                pass
        
        super().save(*args, **kwargs)
        
        # Only update points if the team actually changed
        if old_team != self.team:
            # Remove points from old team if it existed
            if old_team:
                old_team_obj = Team.objects.get(name=old_team)
                old_team_obj.points -= self.points
                old_team_obj.save()
            
            # Add points to new team if it exists
            if self.team:
                new_team_obj = Team.objects.get(name=self.team)
                new_team_obj.points += self.points
                new_team_obj.save()
                
                # Create score log
                ScoreLog.objects.create(
                    team=self.team,
                    points=self.points,
                    event=f"{self.game.name} - {self.award_name}",
                    opponent='All',
                    reason="Special Award"
                )
