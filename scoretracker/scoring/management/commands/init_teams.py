from django.core.management.base import BaseCommand
from scoring.models import Team

class Command(BaseCommand):
    help = 'Initialize teams with default colors and zero points'

    def handle(self, *args, **options):
        teams_data = [
            {'name': 'shinobi', 'color': '#DC2626', 'points': 0},
            {'name': 'pegasus', 'color': '#FACC15', 'points': 0},
            {'name': 'chimera', 'color': '#1E1B4B', 'points': 0},
            {'name': 'phoenix', 'color': '#F97316', 'points': 0},
        ]
        
        for team_data in teams_data:
            team, created = Team.objects.get_or_create(
                name=team_data['name'],
                defaults={'color': team_data['color'], 'points': team_data['points']}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created team: {team.get_name_display()}'))
            else:
                self.stdout.write(self.style.WARNING(f'Team already exists: {team.get_name_display()}'))
        
        self.stdout.write(self.style.SUCCESS('Team initialization complete!'))
