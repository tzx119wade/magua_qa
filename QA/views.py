from django.shortcuts import render

# Create your views here.
def proflie(request):
    return render(request, 'profile.html')

def login(request):
    return render(request, 'login.html')

def home(request):
    return render(request, 'home.html')
