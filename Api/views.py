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

@require_POST
@csrf_exempt
def user_register(request):
    if request.user.is_authenticated:
        return JsonResponse({'data': 'You are already logged in', 'status': 400})

    username = request.POST.get('username')
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    email = request.POST.get('email')
    password = request.POST.get('password')
    re_password = request.POST.get('re_password')
    is_active = request.POST.get('is_active')
    is_staff = request.POST.get('is_staff')
    is_superuser = request.POST.get('is_superuser')
    is_artist = request.POST.get('is_artist')

    user = CustomUser.objects.filter(username=username)
    if user.exists():
        return JsonResponse({'data': 'Username already exists!', 'status': 400})

    if password == re_password:
        try:
            user = CustomUser.objects.create_user(username=username, password=password, email=email,
                                                  first_name=first_name, last_name=last_name, is_active=int(is_active),
                                                  is_staff=int(is_staff), is_superuser=int(is_superuser),
                                                  is_artist=int(is_artist))
            login(request, user)
            return JsonResponse({'data': 'registered successfully.', 'status': 200})

        except Exception as e:
            return JsonResponse({'data': 'invalid data', 'status': 400})
    else:
        return JsonResponse({'data': 'Passwords not match!', 'status': 400})



    
@require_GET
@csrf_exempt
def user_data(request, user_id):
    try:
        user = CustomUser.objects.get(pk=user_id)
        serialized_user = serializers.serialize('json', [user])
        return JsonResponse({'data': serialized_user, 'status': 200})
    except:
        return JsonResponse({'data': 'user does not exits!', 'status': 404})


    

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


@require_POST
@csrf_exempt
def media_create(request):
    title = request.POST.get('title')
    media_type = request.POST.get('type')
    artist_id = request.POST.get('artist_id')
    file = request.POST.get('file')
    genre = request.POST.get('genre')
    description = request.POST.get('description')
    lyrics = request.POST.get('lyrics')

    try:
        media = Media.objects.create(title=title, type=media_type, artist_id=artist_id,
                                     file=file, genre=genre, description=description, lyrics=lyrics)
        serialized_media = serializers.serialize('json', [media])
        return JsonResponse({'data': serialized_media, 'status': 200})
    except Exception as e:
        return JsonResponse({'data': 'invalid data', 'status': 400})



@require_POST
@csrf_exempt
def favorite_create(request):
    title = request.POST.get('title')
    user_id = request.POST.get('user_id')

    try:
        favorite = Favorite.objects.create(title=title, user_id=user_id)
        serialized_favorite = serializers.serialize('json', [favorite])
        return JsonResponse({'data': serialized_favorite, 'status': 200})
    except Exception as e:
        return JsonResponse({'data': 'invalid data', 'status': 400})


@require_POST
@csrf_exempt
def add_media_to_favorite(request, favorite_id):
    media_id = request.POST.get('media_id')

    favorite = Favorite.objects.filter(pk=favorite_id)
    if favorite.exists():
        favorite = favorite.first()
        favorite.medias.add(media_id)
        return JsonResponse({'data': 'the favorite data updated successfully.', 'status': 200})
    else:
        return JsonResponse({'data': 'favorite does not exits!', 'status': 404})


@require_GET
@csrf_exempt
def favorite_data(request, favorite_id):
    try:
        favorite = Favorite.objects.get(pk=favorite_id)
        serialized_favorite = serializers.serialize('json', [favorite])
        return JsonResponse({'data': serialized_favorite, 'status': 200})
    except:
        return JsonResponse({'data': 'favorite does not exits!', 'status': 404})


@require_POST
@csrf_exempt
def comment_create(request):
    text = request.POST.get('text')
    user_id = request.POST.get('user_id')
    media_id = request.POST.get('media_id')

    try:
        comment = Comment.objects.create(text=text, user_id=user_id, media_id=media_id)
        serialized_comment = serializers.serialize('json', [comment])
        return JsonResponse({'data': serialized_comment, 'status': 200})
    except Exception as e:
        return JsonResponse({'data': 'invalid data', 'status': 400})


@require_POST
@csrf_exempt
def add_like(request, media_id):
    media = Media.objects.filter(pk=media_id)
    if media.exists():
        media = media.first()
        media.like += 1
        media.save()
        return JsonResponse({'data': 'the media data updated successfully.', 'status': 200})
    else:
        return JsonResponse({'data': 'media does not exits!', 'status': 404})
