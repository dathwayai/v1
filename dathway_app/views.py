from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404,  redirect
from django.contrib.auth.models import User
from django.contrib import auth
from .models import Profile 
from django.db.models import Max
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.shortcuts import render
from .models import ChatMessage
from openai import OpenAI
import os
import re

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", ""))

def extract_tech_skills(bot_response):
    # Try to match the first pattern with compatibility ratings in parentheses
    pattern1 = r'\*\*(.*?)\*\*.*?Compatibility: (\d+)/10'
    matches1 = re.findall(pattern1, bot_response)

    # If the first pattern doesn't match, try a different pattern without parentheses
    if not matches1:
        pattern2 = r'\*\*(.*?)\*\*.*?Compatibility: (\d+)/10'
        matches2 = re.findall(pattern2, bot_response)
        return [{'skill': match[0], 'compatibility': int(match[1])} for match in matches2]

    return [{'skill': match[0], 'compatibility': int(match[1])} for match in matches1]


def get_chat_messages(user_profile, dathway_profile):
    chat_messages = ChatMessage.objects.filter(participants=user_profile).filter(participants=dathway_profile)
    chat_messages = chat_messages.annotate(last_message_time=Max('timestamp')).order_by('last_message_time')

    formatted_messages = []

    formatted_messages.append({"role": "system", "content": "You are a tech career assistant. You chat with users and you ask them 5 questions about their socio-activities and academic background to help them decipher what tech skill they should learn. At the end suggest 5 tech skills and rate them according to their compatibility with the person over 10. Remember to write the skills as a dictionary when giving the final result"})

    for message in chat_messages:
        role = 'user' if message.sender == user_profile else 'assistant'
        formatted_message = {"role": role, "content": message.message}
        formatted_messages.append(formatted_message)

    return formatted_messages

@csrf_exempt
def chat(request):
    print("entered")
    if request.method == 'POST':
        profile = Profile.objects.get(user=request.user)
        dathway = Profile.objects.get(username='dathway')
        user_message = request.POST.get('text', '')
        #print(user_message)
        new_chat = ChatMessage.objects.create(message=user_message, sender=profile)
        new_chat.participants.add(profile)
        new_chat.participants.add(dathway)
        new_chat.save()
        # Append user message to the chat messages list
        formatted_messages = get_chat_messages(profile, dathway)
        formatted_messages.append({"role": "user", "content": user_message})
       #print(formatted_messages)

        completion = client.chat.completions.create(
            model="ft:gpt-3.5-turbo-0613:dathway::8qFUMuKc",
            messages=formatted_messages
        )
    
        bot_response = completion.choices[0].message.content
        # Append assistant (Dathway) response to the chat messages list
        formatted_messages.append({"role": "assistant", "content": bot_response})
        #print(bot_response)
        print(extract_tech_skills(bot_response))

        bot_chat = ChatMessage.objects.create(message=bot_response, sender=dathway, )
        bot_chat.participants.add(profile)
        bot_chat.participants.add(dathway)
        bot_chat.save()
        return JsonResponse({'message': 'success', 'bot_response': bot_response})
    else:
        return JsonResponse({'message': 'error', 'error': 'Invalid request method'})

def dashboard(request):
     profile = Profile.objects.get(user=request.user)
     messages = ChatMessage.objects.filter(participants=profile)
     messages = messages.annotate(last_message_time=Max('timestamp'))
     messages = messages.order_by('last_message_time')
     context = {
         "profile": profile,
         "messages": messages
     }
     return render(request, 'dashboard.html', context)

@csrf_exempt
def home(request):
    return render(request, 'home.html')

def index(request):
     return render(request, 'index.html')

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
