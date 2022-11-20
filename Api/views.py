from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers


@require_POST
@csrf_exempt
def user_login(request):
    if request.user.is_authenticated:
        return JsonResponse({'data':'You are already logged in', 'status':400})

    username = request.POST.get('username')
    password = request.POST.get('password')
    if username and password:
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return JsonResponse({'data':'logged in successfully', 'status':200})

    return JsonResponse({'data':'invalid Username or Password!', 'status':400})
    

	@require_GET
@csrf_exempt
def artist_data(request, artist_id):
    try:
        artist = Artist.objects.get(pk=artist_id)
        serialized_artist = serializers.serialize('json', [artist])
        return JsonResponse({'data': serialized_artist, 'status': 200})
    except:
        return JsonResponse({'data': 'artist does not exits!', 'status': 404})


@require_POST
@csrf_exempt
def artist_edit(request, artist_id):
    country = request.POST.get('country')
    bio = request.POST.get('bio')
    genre = request.POST.get('genre')

    artist = Artist.objects.filter(pk=artist_id)
    if artist.exists():
        artist = artist.first()
        artist.country = country if country else artist.country
        artist.bio = bio if bio else artist.bio
        artist.genre = genre if genre else artist.genre
        artist.save()
        return JsonResponse({'data': 'the artist data updated successfully.', 'status': 200})
    else:
        return JsonResponse({'data': 'artist does not exits!', 'status': 404})
