from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import Team

# Simple password - change this to whatever you want
ADMIN_PASSWORD = "ZRC2026!intramsnibright"

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
    return render(request, 'admin_dashboard.html', {'teams': teams})

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
def add_points(request):
    """API endpoint to add points to a team."""
    team_name = request.POST.get('team')
    points = request.POST.get('points')
    
    if not team_name or not points:
        return JsonResponse({'success': False, 'message': 'missing team or points'}, status=400)
    
    try:
        points = int(points)
        if points < 1:
            return JsonResponse({'success': False, 'message': 'points must be positive'}, status=400)
        
        team = Team.objects.get(name=team_name)
        team.points += points
        team.save()
        
        return JsonResponse({
            'success': True,
            'message': f'Added {points} points to {team.get_name_display()}!',
            'team': team_name,
            'new_total': team.points
        })
    except Team.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'team not found'}, status=404)
    except ValueError:
        return JsonResponse({'success': False, 'message': 'invalid point value'}, status=400)

@require_http_methods(["POST"])
def reset_scores(request):
    """API endpoint to reset all team scores to 0."""
    Team.objects.all().update(points=0)
    return JsonResponse({'success': True, 'message': 'All scores have been reset to 0'})
