from django.shortcuts import render

# Create your views here.
def home(request):
	return render(request, 'home.html')

def login(request):
	return render(request, 'login.html')

def signup(request):
	return render(request,'signup.html')
	
def dashboard(request):
	return render(request,'dashboard.html')

def certificate(request,pk):
	return render(request,'certificate.html')