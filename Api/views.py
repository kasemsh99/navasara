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



@require_POST
@csrf_exempt
def artist_search(request):
    links_lookup = Q()
    if country := request.POST.get('country'):
        links_lookup &= Q(country=country)
    if genre := request.POST.get('genre'):
        links_lookup &= Q(genre=genre)
    if first_name := request.POST.get('first_name'):
        links_lookup &= Q(user__first_name__contains=first_name)
    if last_name := request.POST.get('last_name'):
        links_lookup &= Q(user__last_name__contains=last_name)
    if username := request.POST.get('username'):
        links_lookup &= Q(user__username__contains=username)

    artists = Artist.objects.filter(links_lookup)
    if artists:
        serialized_user = serializers.serialize('json', artists)
        return JsonResponse({'data': serialized_user, 'status': 200})

    return JsonResponse({'data': 'No Artists Found!', 'status': 404})



@require_POST
@csrf_exempt
def media_search(request):
    links_lookup = Q()
    if title := request.POST.get('title'):
        links_lookup &= Q(title__contains=title)
    if media_type := request.POST.get('type'):
        links_lookup &= Q(type=media_type)
    if artist_first_name := request.POST.get('artist_first_name'):
        links_lookup &= Q(artist__user__first_name__contains=artist_first_name)
    if artist_last_name := request.POST.get('artist_last_name'):
        links_lookup &= Q(artist__user__last_name__contains=artist_last_name)
    if genre := request.POST.get('genre'):
        links_lookup &= Q(genre=genre)

    medias = Media.objects.filter(links_lookup)
    if medias:
        serialized_user = serializers.serialize('json', medias)
        return JsonResponse({'data': serialized_user, 'status': 200})

    return JsonResponse({'data': 'No Artists Found!', 'status': 404})
