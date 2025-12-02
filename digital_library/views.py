from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from  django.core.files.storage import FileSystemStorage
from .models import *
from django.utils import timezone
import datetime

def first(request):
    return render(request,'index.html')

def index(request):
    return render(request,'index.html')

def reg(request):
     return render(request,'register.html')

def addreg(request):
    if request.method == "POST":
            name=request.POST.get('name')
            email=request.POST.get('email') 
            phone=request.POST.get('phone')
            password=request.POST.get('password')
            reg_no=request.POST.get('reg_no')
        
            x=register(name=name,email=email,phone=phone,password=password,reg_no=reg_no,status='pending')
            x.save()
    return render(request, 'index.html')



def viewuser(request):
     sel=register.objects.all()
     return render(request,'viewuser.html',{'result':sel})

def useraccept(request,id):
    s=register.objects.get(pk=id)
    s.status='accepted'
    s.save()
    return redirect(viewuser)
    
    
def userreject(request,id):
    s=register.objects.get(pk=id)
    s.status='rejected'
    s.save()
    return redirect(viewuser)


def deleteuser(request,id):
    sel=register.objects.get(id=id)
    sel.delete()
    return redirect(first)

def login(request):
     return render(request,'login.html')
    




from django.utils import timezone
from .models import Logout_tbl, login_tbl  # Import your models

def logout(request):
    session_keys = list(request.session.keys())
    user_id = None
    system_no = None
    
    # Get the user_id and system_no from the session
    if 'user_id' in request.session:
        user_id = request.session['user_id']
    if 'system_no' in request.session:
        system_no = request.session['system_no']
    
    # Create a new instance of Logout_tbl
    logout_instance = Logout_tbl(
        status='Logged Out',
        time = datetime.datetime.now(),  # Current time
        date=timezone.now().date(),  # Current date
        system_no=system_no,  # Get system number from session
        user_id=request.session['uid']  # Get user ID from session
    )
    logout_instance.save()  # Save the instance

    # Clear the session
    for key in session_keys:
        del request.session[key]

    return redirect(first)  # Redirect to 'first' URL





def adlog(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    
    if email == "admin@gmail.com" and password == "admin":
        request.session['logint'] = email
        return render(request, 'index.html')
    else:
        return render(request,'log1.html')

from django.shortcuts import render
from django.utils import timezone
from .models import register, login_tbl, Attendance

def addlogin(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    
    if email == "admin@gmail.com" and password == "admin":
        request.session['logint'] = email
        return render(request, 'index.html')
    
    elif register.objects.filter(email=email, password=password,status="accepted").exists():
        user = register.objects.get(email=email, password=password)
        request.session['uid'] = user.id
        
        current_time = timezone.now()
        system_no = request.POST.get('system_no')
        request.session['system_no'] = system_no
        
        # Create a new login_tbl entry
        ins = login_tbl.objects.create(
            status="logined",
            time=datetime.datetime.now(),  # Save only the time component
            date=current_time.date(),  # Save only the date component
            system_no=system_no,
            user_id=user.id,
            attendence="present"  # Mark attendance as "present"
        )
        
        # Create a new Attendance record
        attendance = Attendance.objects.create(
            user=user,
            login_time=timezone.now(),
            system_no=system_no,
            status="present"  # Mark status as "present"
        )
        
        return render(request, 'index.html')
    
    else:
        return render(request, 'login.html', {'error': 'Invalid login credentials'})



def viewattend(request):
     sel=Attendance.objects.all()
     user= register.objects.all()
     for i in sel:
            for j in user:
                if str(i.user_id)==str(j.id):
                    i.user_id=j.name

     return render(request,'attend.html',{'result':sel})



def stat(request):
     sel=login_tbl.objects.all()
     sel1=Logout_tbl.objects.all()
     user= register.objects.all()
     for i in sel:
            for j in user:
                if str(i.user_id)==str(j.id):
                    i.user_id=j.name

     for i in sel1:
            for j in user:
                if str(i.user_id)==str(j.id):
                    i.user_id=j.name               

     return render(request,'log.html',{'result':sel,'res':sel1})

def viewaddassi(request):
     sel=assignment_tbl.objects.all()
     user= register.objects.all()
     for i in sel:
            for j in user:
                if str(i.user_id)==str(j.id):
                    i.user_id=j.name

     return render(request,'viewaddassi.html',{'result':sel})

def assi(request):
     return render(request,'assignm.html')

def addassi(request):
     if request.method=="POST":
          date=request.POST.get('date')
          reg_no=request.POST.get('reg_no')
          myfile=request.FILES['report']
          fs=FileSystemStorage()
          filename=fs.save(myfile.name,myfile)
          ins=assignment_tbl(date=date,report=filename,reg_no=reg_no,user_id=request.session['uid'])
          ins.save()
     return render(request,'index.html')     



def logggg(request):
    session_keys=list(request.session.keys())
    for key in session_keys:
          del request.session[key]
    return redirect(first)


