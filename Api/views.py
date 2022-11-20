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
    