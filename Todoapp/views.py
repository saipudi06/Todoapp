from Todo.settings import EMAIL_HOST_USER
from django.shortcuts import  render, redirect
from .forms import Newform, Todoform
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import send_mail
# Create your views here.
def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method=='POST':
        form = Newform(request.POST)
        if form.is_valid():
            username=form.cleaned_data.get('username')
            email=form.cleaned_data.get('email')
            body="welcome to Todo community"
            subject=f'hi, {username} ...have a good day'
            email_from= settings.EMAIL_HOST_USER
            send_mail(body,subject,email_from,[email])
            user = form.save()
            login(request, user)
            messages.success(request,"successfull")
            return render(request,'index.html')
        messages.error(request, ' enter valid details ')
    form= Newform()
    return render(request, 'register.html',context={"register_form":form})
    
def login_req(request):
    if request.method=='POST':
        form=AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password')
            user=authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"you logged in as {username}")
                return render(request, 'index.html')
            else:
                messages.error(request, 'Invalid username or password')
        else:
            messages.error(request, 'Invalid username or password')
    form = AuthenticationForm()
    return render(request, "login.html", context={"login_form":form})

def logout_request(request):
    logout(request)
    return render(request, 'logout.html')

@login_required(login_url='/')  
def index(request):
    mydict={
        'alltodo': Todo.objects.all()
    }
    return render(request, 'index.html', context=mydict)

@login_required(login_url='/')  
def add(request):
    
    return render(request, 'add.html')


@login_required(login_url='/')  
def submit(request):
    user=request.user
    if request.method == 'POST':
        messages.info(request, 'task added successfully')
        obj = Todo()
        obj.title= request.POST['title']
        obj.description=request.POST['description']
        obj.date=request.POST['date']
        obj.priority=request.POST['priority']
        obj.user=user
        obj.save()
    todos=Todo.objects.filter(user=user).order_by('created_at')
    return render(request, 'submit.html', context={'alltodo': todos})

@login_required(login_url='/')  
def delete(request, id):
    user=request.user
    obj= Todo.objects.get(id=id)

    obj.delete()
    mydict={
        'alltodo': Todo.objects.filter(user=user)
    }
    return render(request, 'submit.html',context=mydict)

@login_required(login_url='/')  
def completed(request, id):
    user=request.user
    obj= Todo.objects.get(id=id)
    obj1=Completed()
    obj1.title= obj.title
    obj1.description=obj.description
    obj1.date=obj.date
    obj1.priority=obj.priority
    obj1.user=obj.user
    obj1.save()
    obj.delete()
    mydict={
        'alltodo': Completed.objects.filter(user=user)
    }
    return render(request, 'completed.html',context=mydict)

@login_required(login_url='/')  
def done(request):
    user=request.user
    mydict={
        'alltodo': Completed.objects.filter(user=user)
    }
    return render(request, 'completed.html',context=mydict)

@login_required(login_url='/')  
def search(request):
    user=request.user
    obj=request.GET['query']
    mydict = {
        'alltodo' : Todo.objects.filter(user=user, title__icontains=obj)
    }
    return render(request, 'submit.html',context=mydict)

@login_required(login_url='/')  
def sort(request):
    user=request.user
    mydict={
        'alltodo': Todo.objects.filter(user=user)
    }
    return render(request, 'sort.html' ,context=mydict)

@login_required(login_url='/')  
def sortdata(request):
    user=request.user
    obj=request.GET['filt']
    mydict={
        'alltodo': Todo.objects.filter(user=user).order_by(obj)
     }
    return render(request, 'sort.html' ,context=mydict)

@login_required(login_url='/')  
def edit(request, id):
    obj=Todo.objects.get(id=id)
    user=request.user
    mydict={
        'title': obj.title,
        'description': obj.description,
        'date': obj.date,
        'priority': obj.priority,
        'id': id, 
        'user': user,
        
    }
    return render(request, 'edit.html' ,context=mydict)

@login_required(login_url='/')  
def update(request, id):
    user=request.user
    obj = Todo(id=id)
    obj.title = request.GET['title']
    obj.description = request.GET['description']
    obj.priority = request.GET['priority']
    obj.date=request.GET['date']
    obj.user=user
    import datetime
    updated_at = datetime.datetime.now()
    obj.created_at = updated_at
    obj.save()
    user=request.user
    mydictionary = {
        "alltodo" : Todo.objects.filter(user=user)
    }
    return render(request,'submit.html',context=mydictionary)

from django.utils.encoding import force_bytes
def password_reset_request(request):
    if request.method== "POST":
        password_reset_form=PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data=password_reset_form.cleaned_data['email']
            users=User.objects.filter(email=data)
            if users.exists():
                for user in users:
                    subject='password change request'
                    template='pasword/mail.txt'
                    c={
                        'email': user.email,
                        'username': user.username,
                        'domain':'127.0.0.1:8000',
                        'site_name':'website',
                        'user':user,
                        'token': default_token_generator.make_token(user),
                        'protocol':'http',
                        'uid':urlsafe_base64_encode(force_bytes(user.pk))
                    }
                    email= render_to_string(template, c)
                    try:
                        send_mail(subject, email, 'venkateshjnv123@gmail.com', [user.email], fail_silently=False)
                    except:
                        return HttpResponse('Invalid')
                    return redirect('password_reset/done/')
    password_reset_form=PasswordResetForm()
    return render(request, 'pasword/password_reset.html', context={'password_reset_form': password_reset_form})