from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail, EmailMessage
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_text
from .models import storecomplain
from django.contrib.auth.decorators import login_required

from dwm.tokens import generate_token
from my_app import settings

# Create your views here.
def index(request):
    return render(request,"index.html")

def awarness(request):
    return render(request,"Awarness.html")

def signup(request):
    if request.method=="POST":
        username=request.POST['name']
        fname=request.POST['fname']
        lname=request.POST['lname']
        email=request.POST['email']
        password=request.POST['pswd']
        cpassword=request.POST['cpswd']

        if User.objects.filter(email=email):
            messages.error(request,"Email already exist")

        if password!=cpassword:
            messages.error(request,"Password doesn't match")


        myuser=User.objects.create_user(username,email,password)
        myuser.first_name = fname
        myuser.last_name = lname


        myuser.save()
        messages.success(request,"Your Account has been successfully created")

        #Welcome Mail

        subject="Welcome to Domestic Waste Management Login!!"
        message="Hello "+myuser.first_name+ " !! \n "+("Welcome to DWMS!! \n "
                                                       "Thank you for visiting our website \n "
                                                       "Get Explore with our DWMS Website.\n\n"
                                                       "Thanking you\n "
                                                       "By\n"
                                                       "DWMS team.")
        from_email=settings.EMAIL_HOST_USER
        to_list=[myuser.email]
        send_mail(subject,message,from_email,to_list,fail_silently=True)

        return redirect("/login")

    return render(request,"signup.html")

def  loginn(request):
    if request.method=="POST":
        username=request.POST['uname']
        password=request.POST['pass1']

        user=authenticate(request,username=username,password=password)

        if user is not None:
            login(request, user)
            fname=user.first_name
            return redirect('/userhome')
        else:
            return redirect("/login")
    return render(request,"login.html")

def signout(request):
    logout(request)
    return redirect("/login")

def userhome(request):
    return render(request,"userhome.html")

@login_required()
def complains(request):
    if request.method =="POST":
        name=request.POST['name']
        complaints = request.POST['complaint']
        location = request.POST['location']
        locationd = request.POST['locationd']

        user=request.user

        dw_query=storecomplain.objects.create(user=user,name=name,email=user.email,complaint=complaints,locat=location,locatd=locationd)
        dw_query.save()

        return redirect("/userhome")

    return render(request,"complain.html")

@login_required()
def preview(request):
    if request.user.is_superuser:
        data = storecomplain.objects.all()
    else:
        data = storecomplain.objects.filter(user=request.user)
    context={"data":data}

    return render(request,"preview_complain.html",context)

def updateData(request,id):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        complaints = request.POST['complaint']
        location = request.POST['location']
        locationd = request.POST['locationd']

        edit=storecomplain.objects.get(id=id)
        edit.name=name
        edit.email=email
        edit.complaints=complaints
        edit.locat=location
        edit.locatd=locationd
        edit.save()
        return redirect("preview")

    d=storecomplain.objects.get(id=id)
    context={"d":d}

    return render(request,"edit.html",context)

def deleteData(request,id):
    data=storecomplain.objects.get(id=id)
    data.delete()
    return redirect("/preview")


