from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import Team, ScoreLog, Game, GameResult, SpecialAward, Contestant
from django.db.models import Q
import json

# Simple password - change this to whatever you want
ADMIN_PASSWORD = "ZRC2026!intramsnibright"

def health_check(request):
    """Lightweight endpoint for uptime monitoring."""
    return HttpResponse("OK", status=200)

def home(request):
    """Display the scoreboard for 4 teams."""
    teams = Team.objects.all().order_by('name')
    teams_dict = {team.name: {'points': team.points, 'color': team.color} for team in teams}
    return render(request, 'home.html', {'teams': teams_dict})

def admin_login(request):
    """Admin login page."""
    if request.session.get('is_admin'):
        return redirect('admin_dashboard')
    
    if request.method == 'POST':
        password = request.POST.get('password')
        if password == ADMIN_PASSWORD:
            request.session['is_admin'] = True
            return redirect('admin_dashboard')
        else:
            return render(request, 'admin_login.html', {'error': 'thats wrong bro.....'})
    
    return render(request, 'admin_login.html')

def admin_dashboard(request):
    """Admin dashboard for managing scores - password protected."""
    if not request.session.get('is_admin'):
        return redirect('admin_login')
    
    teams = Team.objects.all().order_by('name')
    
    # Get all active games organized by type and category
    all_games = Game.objects.filter(is_active=True).order_by('type', 'category', 'name')
    sports_games = Game.objects.filter(type='sports', is_active=True).order_by('category', 'name')
    litmus_games = Game.objects.filter(type='litmus', is_active=True).order_by('category', 'name')
    minigames = Game.objects.filter(type='minigame', is_active=True).order_by('name')
    
    # Get all game results
    game_results = GameResult.objects.all().select_related('game')
    
    return render(request, 'admin_dashboard.html', {
        'teams': teams,
        'all_games': all_games,
        'sports_games': sports_games,
        'litmus_games': litmus_games,
        'minigames': minigames,
        'game_results': game_results,
    })

def admin_logout(request):
    """Logout from admin dashboard."""
    request.session.flush()
    return redirect('home')

@require_http_methods(["GET"])
def get_scores(request):
    """API endpoint to get current scores for all teams."""
    teams = Team.objects.all().values('name', 'points', 'color')
    return JsonResponse(list(teams), safe=False)

@require_http_methods(["POST"])
def add_game_result(request):
    """API endpoint to add a game result with automatic point calculation."""
    if not request.session.get('is_admin'):
        return JsonResponse({'success': False, 'message': 'Unauthorized'}, status=401)
    
    team_name = request.POST.get('team')
    game_id = request.POST.get('game_id')
    placement = request.POST.get('placement')
    
    if not team_name or not game_id or not placement:
        return JsonResponse({'success': False, 'message': 'Missing required fields'}, status=400)
    
    try:
        game = Game.objects.get(id=game_id)
        placement_int = int(placement)
        
        # Calculate points based on placement
        points_map = {
            1: game.points_1st,
            2: game.points_2nd,
            3: game.points_3rd,
            4: game.points_4th,
            5: game.points_dq,
        }
        points = points_map.get(placement_int, 0)
        
        # Update or create game result
        game_result, created = GameResult.objects.update_or_create(
            game=game,
            team=team_name,
            defaults={'placement': placement_int}
        )
        
        # Update team points
        team = Team.objects.get(name=team_name)
        team.points += points
        team.save()
        
        # Create log entry
        placement_names = {1: '1st', 2: '2nd', 3: '3rd', 4: '4th', 5: 'DQ'}
        ScoreLog.objects.create(
            team=team_name,
            points=points,
            opponent='All',
            event=game.name,
            team_score=placement_int,
            reason=f"Placement: {placement_names.get(placement_int, placement_int)}"
        )
        
        return JsonResponse({
            'success': True,
            'message': f'Added {points} points to {team.get_name_display()} for {placement_names.get(placement_int)} place in {game.name}!',
            'team': team_name,
            'new_total': team.points
        })
    except Game.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Game not found'}, status=404)
    except Team.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Team not found'}, status=404)
    except ValueError:
        return JsonResponse({'success': False, 'message': 'Invalid placement value'}, status=400)


@require_http_methods(["POST"])
def add_points(request):
    """API endpoint to add points to a team."""
    if not request.session.get('is_admin'):
        return JsonResponse({'success': False, 'message': 'Unauthorized'}, status=401)
    
    team_name = request.POST.get('team')
    points = request.POST.get('points')
    opponent = request.POST.get('opponent', '').strip()
    event = request.POST.get('event', '').strip()
    team_score = request.POST.get('team_score', '0').strip()
    opponent_score = request.POST.get('opponent_score', '0').strip()
    reason = request.POST.get('reason', '').strip()
    
    if not team_name or not points:
        return JsonResponse({'success': False, 'message': 'missing team or points'}, status=400)
    
    if not event:
        return JsonResponse({'success': False, 'message': 'event name is required'}, status=400)
    
    try:
        points = int(points)
        
        # Require reason for negative points
        if points < 0 and not reason:
            return JsonResponse({'success': False, 'message': 'reason is required for deductions'}, status=400)
        
        team_score_int = int(team_score) if team_score else 0
        opponent_score_int = int(opponent_score) if opponent_score else 0
        
        team = Team.objects.get(name=team_name)
        # Only update points if non-zero
        if points != 0:
            team.points += points
            team.save()
        
        # Create log entry
        ScoreLog.objects.create(
            team=team_name,
            points=points,
            opponent=opponent if opponent else None,
            event=event,
            team_score=team_score_int,
            opponent_score=opponent_score_int if opponent else None,
            reason=reason if reason else None
        )
        
        # Special message for 0 points (logging only)
        if points == 0:
            return JsonResponse({
                'success': True,
                'message': f'Logged match result for {team.get_name_display()}!',
                'team': team_name,
                'new_total': team.points
            })
        
        action = "Deducted" if points < 0 else "Added"
        abs_points = abs(points)
        return JsonResponse({
            'success': True,
            'message': f'{action} {abs_points} points {"from" if points < 0 else "to"} {team.get_name_display()}!',
            'team': team_name,
            'new_total': team.points
        })
    except Team.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'team not found'}, status=404)
    except ValueError:
        return JsonResponse({'success': False, 'message': 'invalid point value'}, status=400)

@require_http_methods(["POST"])
def reset_scores(request):
    """API endpoint to reset all team scores to 0 and clear all logs."""
    if not request.session.get('is_admin'):
        return JsonResponse({'success': False, 'message': 'Unauthorized'}, status=401)
    
    Team.objects.all().update(points=0)
    ScoreLog.objects.all().delete()
    return JsonResponse({'success': True, 'message': 'All scores and logs have been reset'})


def leaderboard(request):
    """Display the public leaderboard page with game results."""
    teams = Team.objects.all().order_by('name')
    
    # Get all active games organized by type and category
    # Exclude esports games from sports
    esports_names = ['Mobile Legends', 'Call of Duty Mobile', 'Valorant']
    sports_games = Game.objects.filter(type='sports', is_active=True).exclude(name__in=esports_names).order_by('category', 'name')
    esports_games = Game.objects.filter(type='sports', name__in=esports_names, is_active=True).order_by('name')
    # Exclude Mr. Pisay and Miss Pisay from litmus_games
    litmus_games = Game.objects.filter(type='litmus', is_active=True).exclude(name__in=['Mr. Pisay', 'Miss Pisay']).order_by('category', 'name')
    mr_miss_pisay = Game.objects.filter(type='litmus', name__in=['Mr. Pisay', 'Miss Pisay'], is_active=True).order_by('name')
    minigames = Game.objects.filter(type='minigame', is_active=True).order_by('name')
    
    # Get special awards for Mr. and Miss Pisay
    special_awards = SpecialAward.objects.filter(game__in=mr_miss_pisay).select_related('game')
    
    return render(request, 'leaderboard.html', {
        'teams': teams,
        'sports_games': sports_games,
        'esports_games': esports_games,
        'litmus_games': litmus_games,
        'mr_miss_pisay': mr_miss_pisay,
        'minigames': minigames,
        'special_awards': special_awards,
    })


def logs(request):
    """Display the logs page with scoring history."""
    return render(request, 'logs.html')


@require_http_methods(["GET"])
def get_logs(request):
    """API endpoint to get all score logs."""
    logs = ScoreLog.objects.all().values('id', 'team', 'points', 'opponent', 'event', 'team_score', 'opponent_score', 'reason', 'timestamp')
    logs_list = []
    
    for log in logs:
        # Get team display name
        team_display = dict(Team.TEAM_CHOICES).get(log['team'], log['team'])
        
        logs_list.append({
            'id': log['id'],
            'team': log['team'],
            'team_display': team_display,
            'points': log['points'],
            'opponent': log['opponent'] if log['opponent'] else 'All',
            'event': log['event'],
            'team_score': log['team_score'],
            'opponent_score': log['opponent_score'],
            'reason': log['reason'],
            'timestamp': log['timestamp'].isoformat()
        })
    
    return JsonResponse(logs_list, safe=False)


@require_http_methods(["POST"])
def set_game_result(request):
    """API endpoint to set game results/placements."""
    if not request.session.get('is_admin'):
        return JsonResponse({'success': False, 'message': 'Unauthorized'}, status=401)
    
    game_id = request.POST.get('game_id')
    placements = request.POST.get('placements')  # JSON string: {"team_name": placement}
    
    if not game_id or not placements:
        return JsonResponse({'success': False, 'message': 'Missing game_id or placements'}, status=400)
    
    try:
        import json
        placements_dict = json.loads(placements)
        game = Game.objects.get(id=game_id)
        
        # Clear existing results for this game
        GameResult.objects.filter(game=game).delete()
        
        # Create new results
        for team_name, placement in placements_dict.items():
            if placement and int(placement) > 0:
                GameResult.objects.create(
                    game=game,
                    team=team_name,
                    placement=int(placement)
                )
        
        return JsonResponse({
            'success': True,
            'message': f'Updated results for {game.name}'
        })
    except Game.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Game not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=400)


@require_http_methods(["GET"])
def get_game_results(request):
    """API endpoint to get all game results."""
    results = GameResult.objects.all().select_related('game')
    results_data = {}
    
    for result in results:
        if result.game.id not in results_data:
            results_data[result.game.id] = {}
        results_data[result.game.id][result.team] = result.placement
    
    return JsonResponse(results_data, safe=False)


@require_http_methods(["POST"])
def add_special_award(request):
    """API endpoint to add a special award."""
    if not request.session.get('is_admin'):
        return JsonResponse({'success': False, 'message': 'Unauthorized'}, status=401)
    
    game_id = request.POST.get('game_id')
    award_name = request.POST.get('award_name')
    team = request.POST.get('team')
    
    if not game_id or not award_name or not team:
        return JsonResponse({'success': False, 'message': 'Missing required fields'}, status=400)
    
    try:
        game = Game.objects.get(id=game_id)
        
        # Create or update award
        award, created = SpecialAward.objects.update_or_create(
            game=game,
            award_name=award_name,
            defaults={'team': team, 'points': 5}
        )
        
        team_display = dict(Team.TEAM_CHOICES).get(team, team)
        message = f"Awarded '{award_name}' to {team_display}!" if created else f"Updated '{award_name}' to {team_display}!"
        
        return JsonResponse({'success': True, 'message': message})
    except Game.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Game not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=400)


@require_http_methods(["GET"])
def get_special_awards(request, game_id):
    """API endpoint to get all special awards for a game."""
    try:
        awards = SpecialAward.objects.filter(game_id=game_id)
        awards_data = []
        
        for award in awards:
            team_display = dict(Team.TEAM_CHOICES).get(award.team, 'TBD') if award.team else 'TBD'
            awards_data.append({
                'id': award.id,
                'award_name': award.award_name,
                'team': award.team,
                'team_display': team_display,
                'points': award.points
            })
        
        return JsonResponse(awards_data, safe=False)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=400)


@require_http_methods(["POST"])
def delete_special_award(request, award_id):
    """API endpoint to clear a special award (set team to None instead of deleting)."""
    if not request.session.get('is_admin'):
        return JsonResponse({'success': False, 'message': 'Unauthorized'}, status=401)
    
    try:
        award = SpecialAward.objects.get(id=award_id)
        
        # Remove points from team if assigned
        if award.team:
            team = Team.objects.get(name=award.team)
            team.points -= award.points
            team.save()
            
            # Clear the team assignment but keep the award
            award.team = None
            award.save()
        
        return JsonResponse({'success': True, 'message': 'Award cleared'})
    except SpecialAward.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Award not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=400)

def mrmspisay_showcase(request):
    """Display the Mr. & Miss Pisay showcase page."""
    contestants = Contestant.objects.filter(is_active=True).order_by('order')
    contestants_data = []
    
    # Get team colors
    teams = Team.objects.all()
    team_colors = {team.name: team.color for team in teams}
    
    for contestant in contestants:
        contestants_data.append({
            'id': contestant.id,
            'name': contestant.name,
            'empire': contestant.empire,
            'empire_display': contestant.get_empire_display(),
            'empire_color': team_colors.get(contestant.empire, '#FFFFFF'),
            'photo_url': contestant.photo.url if contestant.photo else '',
            'video_url': contestant.advocacy_video.url if contestant.advocacy_video else '',
        })
    
    return render(request, 'mrmspisay.html', {
        'contestants': contestants,
        'contestant_names_json': json.dumps(contestants_data),
        'team_colors': json.dumps(team_colors)
    })
