from sre_constants import SUCCESS
from django.shortcuts import render ,redirect,HttpResponse 
from app.EmailBackEnd import EmailBackEnd
from django.contrib.auth import  authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from app.models import CustomUser
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
def BASE(request):
    return render(request,'base.html')


#Login

def LOGIN(request):
    return render(request,'login.html')
@csrf_exempt
def doLogin(request):
    if request.method == "POST":
        user = EmailBackEnd.authenticate(request,username=request.POST.get('email'),password=request.POST.get('password'),)
        if user!=None:
            login(request,user)
            user_type = user.user_type
            if  user_type == '1':
                return redirect('hod_home')
            elif user_type == '2':
                return redirect('staff_home')
            elif user_type == '3':
                return HttpResponse('This is a Student Pannel')
            else:
                 messages.error(request, "Email and password Are invalid")
                 #return HttpResponse('This is a Else Pannel')
                 return redirect('login')
        else:
            #message
            messages.error(request, "Email and password Are invalid 2")
            return redirect('login')
            # data = {
            #     'message' : 'Email and password Are invalid' 
            # }
            #return JsonResponse(data)
    else:
         return redirect('login')
        
#Logout
def doLogout(request):
    logout(request)
    return redirect('login')


#profile
def PROFILE(request):
    user = CustomUser.objects.get(id=request.user.id)
    print("profile",user)
    context = {
        "user":user
    }
    return render(request,'profile.html',context)


#PORFILE UPDATE
@login_required(login_url='/')
def PROFILE_UPDATE(request):
    if request.method == "POST":
        profile_pic = request.FILES.get('profile_pic')
        print(profile_pic)
        first_name = request.POST.get('first_name')
        last_name = request.POST['last_name']
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(profile_pic,first_name, last_name, email,username,password)
        try:
            customuser = CustomUser.objects.get(id = request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name     
            if password !=None and password !="":
                customuser.set_password(password)
            if profile_pic !=None and profile_pic !="":
                customuser.profile_pic = profile_pic                    
            customuser.save()
            messages.success(request,"Your Profile Update Successfully")
            return redirect('profile')
        except:
            messages.error(request,"Failed To Update Your Profile")


    return render(request,'profile.html')
    
