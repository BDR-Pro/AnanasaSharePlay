from django.shortcuts import redirect
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
    
def is_user_authenticated(request):
    if request.user.is_authenticated:
        return JsonResponse({'message': 'User is authenticated'})
    else:
        return JsonResponse({'message': 'User is not authenticated'}, status=401)
    
def register_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            email = data.get('email')
            password = data.get('password')
            avatar = data.get('avatar')
            nickname = data.get('nickname')
            print(data)
            
            # Validation
            if not all([email, password, avatar, nickname]):
                return JsonResponse({'message': 'Missing required fields'}, status=400)

            # Password hashing
            user = AuthUser.objects.create_user(email=email, password=password)

            # Create UserProfile
            UserProfile.objects.create(user=user, avatar=avatar, nickname=nickname)

            # Authenticate the user
            auth_user = authenticate(request, email=email, password=password)
            if auth_user is not None:
                login(request, auth_user)
                return JsonResponse({'message': 'Registration successful'})
            else:
                return JsonResponse({'message': 'Invalid credentials'}, status=401)
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON data'}, status=400)
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=405)
    
def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('/')