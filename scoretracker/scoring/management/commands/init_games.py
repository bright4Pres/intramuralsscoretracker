from django.core.management.base import BaseCommand
from scoring.models import Game


class Command(BaseCommand):
    help = 'Initialize all games/events with their categories and points systems'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating games...')
        
        games_data = []
        
        # Minigames - using Major points system as default
        minigames = [
            'Mario Kart',
            'Block Blast',
            'Uno',
            'Super Mario Party',
            'Subway Surfers',
            'Code Names',
            'Super Smash Bros',
            'Jenga',
            'Rubiks Cube',
            'Google Dinosaur',
            'Watermelon Game',
            'Chain Reaction',
        ]
        
        for game in minigames:
            games_data.append({
                'name': game,
                'category': 'minigame',
                'type': 'minigame',
                'points_1st': 1,
                'points_2nd': 0,
                'points_3rd': 0,
                'points_4th': 0,
                'points_dq': 0,
            })
        
        # LITMUS - Major Events
        litmus_major = [
            'Major',
            'Neo-Ethnic Dance',
            'Saludo',
            'Speech Choir',
        ]
        
        for game in litmus_major:
            games_data.append({
                'name': game,
                'category': 'major',
                'type': 'litmus',
                'points_1st': 20,
                'points_2nd': 16,
                'points_3rd': 12,
                'points_4th': 8,
                'points_dq': 5,
            })
        
        # Mr. and Ms. Pisay - Special case
        games_data.append({
            'name': 'Mr. and Ms. Pisay',
            'category': 'major',
            'type': 'litmus',
            'points_1st': 20,
            'points_2nd': 16,
            'points_3rd': 12,
            'points_4th': 8,
            'points_dq': 5,
            'notes': '4 special awards: 5 points per award'
        })
        
        # LITMUS - Minor Events
        litmus_minor = [
            'Extemporaneous Speech',
            'Quiz Bowl',
            'Vocal Solo',
            'Vocal Duet',
            'Talumpati',
        ]
        
        for game in litmus_minor:
            games_data.append({
                'name': game,
                'category': 'minor',
                'type': 'litmus',
                'points_1st': 15,
                'points_2nd': 12,
                'points_3rd': 9,
                'points_4th': 6,
                'points_dq': 3,
            })
        
        # Sports - Major Events
        sports_major = [
            "Volleyball Men's",
            "Volleyball Women's",
            "Basketball Men's",
            'Track and Field Relay',
        ]
        
        for game in sports_major:
            games_data.append({
                'name': game,
                'category': 'major',
                'type': 'sports',
                'points_1st': 20,
                'points_2nd': 16,
                'points_3rd': 12,
                'points_4th': 8,
                'points_dq': 5,
            })
        
        # Sports - Minor Events
        sports_minor = [
            "Basketball Women's",
            "Pickleball Double's Women's Faculty",
            "Pickleball Double's Men's Faculty",
            "Pickleball Double's Women's Student",
            "Pickleball Double's Men's Student",
            "Pickleball Double's Women's Faculty",  # Listed twice in original
            "Pickleball Mixed Double's",
            "Badminton Singles Women's",
            "Badminton Singles Men's",
            'Badminton Mixed Doubles',
            "Tabletennis Singles Men's",
            "Tabletennis Singles Women's",
            'Tabletennis Mixed Doubles',
            'Mobile Legends',
            'Call of Duty Mobile',
            'Valorant',
            'Chess',
            'Track and Field Dash',
        ]
        
        for game in sports_minor:
            games_data.append({
                'name': game,
                'category': 'minor',
                'type': 'sports',
                'points_1st': 15,
                'points_2nd': 12,
                'points_3rd': 9,
                'points_4th': 6,
                'points_dq': 3,
            })
        
        # Create or update games
        created_count = 0
        updated_count = 0
        
        for game_data in games_data:
            game, created = Game.objects.update_or_create(
                name=game_data['name'],
                defaults={
                    'category': game_data['category'],
                    'type': game_data['type'],
                    'points_1st': game_data['points_1st'],
                    'points_2nd': game_data['points_2nd'],
                    'points_3rd': game_data['points_3rd'],
                    'points_4th': game_data['points_4th'],
                    'points_dq': game_data['points_dq'],
                    'notes': game_data.get('notes', ''),
                    'is_active': True,
                }
            )
            
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'Created: {game.name}'))
            else:
                updated_count += 1
                self.stdout.write(self.style.WARNING(f'Updated: {game.name}'))
        
        self.stdout.write(self.style.SUCCESS(
            f'\nFinished! Created {created_count} games, Updated {updated_count} games'
        ))
