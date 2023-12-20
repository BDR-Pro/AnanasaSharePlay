from django.shortcuts import render , redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User as AuthUser
from shareplay.models import UserProfile
import json
from django.http import JsonResponse

def login_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')
            auth = authenticate(email=email, password=password)
            if auth is not None:
                login(request, auth)
                return JsonResponse({'message': 'Login successful'})
            else:
                return JsonResponse({'message': 'Invalid credentials'}, status=401)
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON data'}, status=400)
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=400)


def register_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')
            avatar = data.get('avatar')
            nickname = data.get('nickname')

            # Validation
            if not all([email, password, avatar, nickname]):
                return JsonResponse({'message': 'Missing required fields'}, status=400)

            # Password hashing
            user = AuthUser.objects.create_user(email=email, password=password)

            # Create UserProfile
            UserProfile.objects.create(user=user, avatar=avatar, nickname=nickname)

            # Authenticate the user
            auth = authenticate(email=email, password=password)
            if auth is not None:
                login(request, auth)
                return JsonResponse({'message': 'Registration successful'})
            else:
                return JsonResponse({'message': 'Invalid credentials'}, status=401)
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON data'}, status=400)
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=400)
    
def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('/')