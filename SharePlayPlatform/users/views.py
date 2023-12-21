from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User as AuthUser
from shareplay.models import UserProfile
import json
from django.http import JsonResponse


def login_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            auth = authenticate(username=username, password=password)
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
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            avatar = request.FILES.get('avatar')
            nickname = request.POST.get('nickname')
            
            # Validation
            if not all([email, password, avatar, nickname]):
                return JsonResponse({'message': 'Missing required fields'}, status=400)
            try:
            # Password hashing
                user = AuthUser.objects.create_user(username=username,email=email, password=password)
            except:
                return JsonResponse({'message': 'Username or email already exists'}, status=400)

            # Create UserProfile
            UserProfile.objects.create(user=user,avatar=avatar, nickname=nickname)

            # Authenticate the user
            auth_user = authenticate(username=username, password=password)
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
    
def profile(request, username):
    try:
        user=AuthUser.objects.get(username=username)
        user_profile = UserProfile.objects.get(user=user)
        user_info = {
            'username': user_profile.user.username,
            'email': user_profile.user.email,
            'avatar': str(user_profile.avatar),  # Assuming avatar is a FileField
            'nickname': user_profile.nickname,
            # Add more fields as needed
        }
        return render(request, 'frontend/profile.html', {'user_info': user_info})
    except UserProfile.DoesNotExist:
        # Handle the case when the user profile does not exist
        return render(request, 'frontend/profile_not_found.html')