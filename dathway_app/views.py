from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404,  redirect
from django.contrib.auth.models import User
from django.contrib import auth
from .models import Profile 


@csrf_exempt
def home(request):
    return render(request, 'home.html')

def index(request):
     return render(request, 'index.html')

def dashboard(request):
     return render(request, 'dashboard.html')

def chat(request):
     return render(request, 'chat.html')

def course(request):
     return render(request, 'course.html')

def analytics(request):
     return render(request, 'analytics.html')

def notifications(request):
     return render(request, 'notifications.html')

def profile(request):
     return render(request, 'profile.html')

def settings(request):
     return render(request, 'settings.html')

@csrf_exempt
def signup(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        username = request.POST.get('username')
        firstname = request.POST.get('first_name')
        lastname = request.POST.get('last_name')
        display_name = firstname + " " + lastname
        
        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'User already exists. '}, status=400)
        else:
            user = User.objects.create_user(username=username, password=password, email=email)
            profile = Profile.objects.create(user=user, username=username, display_name = display_name )
            auth.login(request, user)
            return JsonResponse({'message': 'success'})
    return redirect('index')

@csrf_exempt
def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(email)
        print(password)
        # print(password)
        if "@" in email:
            user = auth.authenticate(email=email, password=password)
        else:
            user = auth.authenticate(username=email, password=password)
        print(user)
        if user is not None:
            auth.login(request, user)
            return JsonResponse({'message': 'success'})
        else:
            return JsonResponse({'error': 'Invalid login credentials, please check your email adress and password.'}, status=400)
    return redirect('index')

@csrf_exempt
def logout(request):
    auth.logout(request)
    return redirect('home')
