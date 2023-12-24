from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User as AuthUser
from shareplay.models import UserProfile
import json
from django.http import HttpResponseNotFound
from django.http import JsonResponse


def login_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            print(data)
            print(request.headers)
            auth = authenticate(username=username, password=password)
            if auth is not None:
                login(request, auth)
                print('message Login successful')
                return JsonResponse({'message': 'Login successful'})
            else:
                print('message Invalid credentials')
                return JsonResponse({'message': 'Invalid credentials'}, status=401)
        except json.JSONDecodeError:
            print('message Invalid JSON data')
            return JsonResponse({'message': 'Invalid JSON data'}, status=400)
    else:
        print('message Invalid request method')
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
    print(request.user)
    if request.user.is_authenticated:
        logout(request)
        return redirect('/')
    
def profile(request, username):
    if username=='undefined':
        return JsonResponse({'message': 'Invalid username'}, status=400)
    if username=="login":
        return login_view(request)
    if username=="logout":
        return logout_view(request)
    if username=="register":
        return register_view(request)
    
    try:
        if UserProfile.objects.get(user=AuthUser.objects.get(username=username)):
            return render(request, 'frontend/profile.html')
    except UserProfile.DoesNotExist:
        # Handle the case when the user profile does not exist
        return HttpResponseNotFound('<h1>Page not found</h1>')
    
def ProfileId(request,id):
    user=UserProfile.objects.get(user=AuthUser.objects.get(id=id))
    return redirect('/users/'+user.user.username)


def getNameById(request,id):
    user=UserProfile.objects.get(user=AuthUser.objects.get(id=id))
    return JsonResponse({'nickname': user.nickname})