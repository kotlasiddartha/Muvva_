
from django.shortcuts import render, redirect
from .models import *
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url="/login/")
def receipes(request):
    if request.method == "POST":
        data = request.POST
        print(data)
 
        case_number = data.get("case_number")
        receipe_name = data.get('receipe_name')
        receipe_description = data.get('receipe_description')
        receipe_image = request.FILES.get('receipe_image')

        print(receipe_name)
        print(receipe_description)
        print(receipe_image)


        Receipe.objects.create(
            case_number = case_number,
            receipe_name = receipe_name,
            receipe_description = receipe_description,
            receipe_image = receipe_image,
        )

        return redirect('/receipes/')
    
    queryset = Receipe.objects.all()

    """below two line are for searching """
    
    if request.GET.get('search'):
        queryset = queryset.filter(receipe_name__icontains = request.GET.get('search'))

    context = {"receipes":queryset}

    return render(request, "home/receipes.html", context)

def update_receipe(request, id):
    queryset = Receipe.objects.get(id = id)
    context = {"receipe":queryset}
    
    if request.method == "POST":
        data = request.POST
        print(data)

        case_number = data.get('case_number')
        receipe_name = data.get('receipe_name')
        receipe_description = data.get('receipe_description')
        receipe_image = request.FILES.get('receipe_image')

        queryset.case_number = case_number
        queryset.receipe_name = receipe_name
        queryset.receipe_description = receipe_description

        if receipe_image:
            queryset.receipe_image = receipe_image
        
        queryset.save()

        return redirect('/receipes/')


    
    return render(request, "home/update_receipes.html", context)

def delete_receipe(request, id):
    queryset = Receipe.objects.get(id = id)
    queryset.delete()
    return redirect('/receipes/')

def login_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if not User.objects.filter(username=username).exists(): #this is to check if username already exists
            messages.error(request,"Invalid username")
            return redirect('/login')
        
        user = authenticate(username=username, password = password)

        if user is None:
            messages.error(request,"Invalid password")
            return redirect('/login')
        else:
            login(request, user)
            return redirect('/receipes/')
        
    return render(request, "home/login.html")

def logout_page(request):
    logout(request)
    return redirect('/login')

def register(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        password = request.POST.get("password")
        

        user = User.objects.filter(username=username) #this is to check if username already exists

        if user.exists():
            messages.info(request, "Username already taken") # Message if username exist
            return redirect('/register/')

        user = User.objects.create(
            first_name = first_name,
            last_name = last_name,
            username = username

        )

        user.set_password(password) #this is for password encryption as the password will be returned as a text.
        user.save()

        messages.info(request, "Account created successfully") # Message if user got created successfully

        return redirect('/login/')


    return render(request, "home/register.html")

    
