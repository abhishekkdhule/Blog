from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
from .models import Articles
from django.core.exceptions import ValidationError
import random
# Create your views here.
def register(request):
    
    if request.method=="POST":
        userid=request.POST['userid']
        firstname=request.POST['firstname']
        lastname=request.POST['lastname']
        pass1=request.POST['password']
        pass2=request.POST['conf-password']
        captcha=request.POST['captcha']
     
        if(pass1==pass2 and len(pass1)>8 and pass1.isalnum()):
            if User.objects.filter(username=userid).exists():
                print('user id exists')
                messages.info(request,'User id exists')
                return redirect('register')
            else:
                user=User.objects.create_user(username=userid,first_name=firstname,last_name=lastname,password=pass1)
                user.save()
                print('user created')
                # messages.info(request,'User Created') 
                return redirect('login')
        else:
            print('password does not match')
            messages.info(request,'1.password length should be>8 | 2.both password should be same | 3.password must be alpha numeric')
            return redirect('register')

        return redirect('login')
    
    else:
        
        return render(request,'homepage/signup.html')

def login(request):
    if request.method=="POST":
        userid=request.POST['userid']
        password=request.POST['password']

        user=auth.authenticate(username=userid,password=password)

        if user!=None:
            auth.login(request,user)
            print("user logged in")
            return redirect('home',user.id)
        else:
            messages.info(request,'invalid credentials')
            return redirect('login')
    else:
        return render(request,'homepage/login.html')
    
def logout(request):
    auth.logout(request)
    return redirect('login')

def AddNewPost(request):
    print("addNewpost called")
    if request.method=="POST":
        a1=Articles()
        u1=request.user
        content=request.POST['article']
        try:
            ispublic=request.POST['ispublic'] 
            ispublic=True  
        except:
            ispublic=False
        try:
            heading=request.POST['heading']
        except:
            heading=None
        try:
            img=request.FILES['img']
        except:
            img=None

        print(u1,content,ispublic,img,heading)
        a1.user=u1
        a1.content=content
        a1.wantpublic=ispublic
        a1.heading=heading
        a1.img=img
        try:
            a1.full_clean()
            a1.save()
        except ValidationError as e:
            print(e)
            messages.info(request,e)

        return redirect('home',u1.id)
        
        



    return render(request,'homepage/addarticle.html')

def feed(request,userid):
    a1=Articles.objects.filter(user=userid)
    print(a1)
    context={
        "posts":a1,
    }
    return render(request,'homepage/home.html',context)
    

def SearchUser(request):
    if request.method=="POST":
        searcheduser=request.POST['searchuser']
        print(searcheduser)
        userobj=User.objects.filter(username=searcheduser)[0]
        print(userobj.id)
        a1=Articles.objects.filter(user=userobj.id).filter(wantpublic=True)
        context={
            "posts":a1,
        }
    return render(request,'homepage/home.html',context)
    