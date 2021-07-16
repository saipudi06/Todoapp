from django.db import models

# Create your models here.
class Todo(models.Model):
    title=models.CharField(max_length=40)
    description= models.CharField(max_length=300)
    date=models.DateField()
    priority=models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    class Meta:  
        db_table = "Todolist"  
    
class Completed(models.Model):
    title=models.CharField(max_length=40)
    description= models.CharField(max_length=300)
    date=models.DateField()
    priority=models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    class Meta:  
        db_table = "completed"  