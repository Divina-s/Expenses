from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User

     
class Expense(models.Model):
    amount=models.FloatField()
    date=models.DateField(default=now)
    description=models.TextField()
    author=models.ForeignKey(to=User, on_delete=models.CASCADE)
    category=models.CharField(max_length=256)


    def __str__(self):
        return self.Category
    class Meta:
        ordering= ['-date']

class Category(models.Model):
    name=models.CharField(max_length=256)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural="Categories"


class Income(models.Model):
    amount=models.FloatField()
    date=models.DateField(default=now)
    description=models.TextField()
    author=models.ForeignKey(to=User, on_delete=models.CASCADE)
    source=models.CharField(max_length=256)


    def __str__(self):
        return self.source
    class Meta:
        ordering= ['-date']
        verbose_name_plural="Income"

class Source(models.Model):
    name=models.CharField(max_length=256)
    
    def __str__(self):
        return self.name
   

    
