from django.shortcuts import render
from django.http import HttpResponse
from .models import *
# Create your views here.
def index(request):
    mydict={
        'alltodo': Todo.objects.all()
    }
    return render(request, 'index.html', context=mydict)

def add(request):
    return render(request, 'add.html')

def submit(request):
    if request.method == 'POST':
        obj = Todo()
        obj.title= request.POST['title']
        obj.description=request.POST['description']
        obj.date=request.POST['date']
        obj.priority=request.POST['priority']
        obj.save()
    mydict={
        'alltodo': Todo.objects.all()
    }
    return render(request, 'submit.html',context=mydict)

def delete(request, id):
    obj= Todo.objects.get(id=id)
    obj.delete()
    mydict={
        'alltodo': Todo.objects.all()
    }
    return render(request, 'submit.html',context=mydict)

def completed(request, id):
    obj= Todo.objects.get(id=id)
    obj1=Completed()
    obj1.title= obj.title
    obj1.description=obj.description
    obj1.date=obj.date
    obj1.priority=obj.priority
    obj1.save()
    obj.delete()
    mydict={
        'alltodo': Completed.objects.all()
    }
    return render(request, 'completed.html',context=mydict)

def done(request):
    mydict={
        'alltodo': Completed.objects.all()
    }
    return render(request, 'completed.html',context=mydict)

def search(request):
    obj=request.GET['query']
    mydict = {
        'alltodo' : Todo.objects.filter(title__icontains=obj)
    }
    return render(request, 'submit.html',context=mydict)

def sort(request):
    mydict={
        'alltodo': Todo.objects.all()
    }
    return render(request, 'sort.html' ,context=mydict)

def sortdata(request):
    obj=request.GET['filt']
    mydict={
        'alltodo': Todo.objects.all().order_by(obj)
     }
    return render(request, 'sort.html' ,context=mydict)

def edit(request, id):
    obj=Todo.objects.get(id=id)
    mydict={
        'title': obj.title,
        'description': obj.description,
        'date': obj.date,
        'priority': obj.priority,
        'id': id, 
        
    }
    return render(request, 'edit.html' ,context=mydict)

def update(request, id):
    obj = Todo(id=id)
    obj.title = request.GET['title']
    obj.description = request.GET['description']
    obj.priority = request.GET['priority']
    obj.date=request.GET['date']
    import datetime
    updated_at = datetime.datetime.now()
    obj.created_at = updated_at
    obj.save()
    mydictionary = {
        "alltodo" : Todo.objects.all()
    }
    return render(request,'submit.html',context=mydictionary)