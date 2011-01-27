from django.db import models
from django.core.files.storage import FileSystemStorage
from settings import *


# Create your models here.
fs = FileSystemStorage(location=STORAGE_PATH + 'pmdb/')

class Manufacturer(models.Model):
    Manufacturer = models.CharField(max_length=200)
    url = models.CharField(max_length=200)
    def __unicode__(self):
        return self.Manufacturer
    
class Housing(models.Model):
    Housing = models.CharField(max_length=200)
    def __unicode__(self):
        return self.Housing

class Category(models.Model):
    Category = models.CharField(max_length=200)
    def __unicode__(self):
        return self.Category

class Unit(models.Model):
    Unit = models.CharField(max_length=50)
    def __unicode__(self):
        return self.Unit

class Project(models.Model):
    Name = models.CharField(max_length=200)
    Description = models.TextField()
    def __unicode__(self):
        return self.Name
    

class Part(models.Model):
    Model = models.CharField(max_length=200)
    Housing = models.ForeignKey(Housing)
    Category = models.ManyToManyField(Category)
    Manufacture = models.ForeignKey(Manufacturer)
    Quantity = models.CharField(max_length=30)
    Description = models.TextField()
    Unit = models.ForeignKey(Unit,null=True, blank=True)
    Amount = models.CharField(max_length=10,null=True,blank=True)
    Datasheet  = models.FileField(storage=fs, upload_to='%Y/%m', null=True, blank=True)
    def __unicode__(self):
        return self.Model

class PartChange(models.Model):
    MAYBECHOICE = (
        ('IN', 'In'),
        ('OUT', 'Out'),
    )
    Part = models.ForeignKey(Part)
    Date = models.DateField(auto_now=True)
    Direction = models.CharField(max_length=3, choices=MAYBECHOICE)
    Quantity = models.CharField(max_length=30)
    Project = models.ForeignKey(Project, null=True, blank=True)
    Supplier = models.CharField(max_length=150, null=True, blank=True)
    Ordernr = models.CharField(max_length=150, null=True, blank=True)
    Description = models.TextField()
    def __unicode__(self):
        return self.Ordernr 
