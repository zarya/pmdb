from django.db import models
from django.core.files.storage import FileSystemStorage
from django.db.models import Avg, Max, Min, Count, Sum
from django.db.models.signals import post_save
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

def update_part(self):
    parts_out = PartChange.objects.filter(Direction='OUT',Part=self.Part_id).aggregate(parts=Sum('Quantity'))
    parts_in = PartChange.objects.filter(Direction='IN',Part=self.Part_id).aggregate(parts=Sum('Quantity'))
    try:
        float(parts_in['parts'])
        parts_in = parts_in['parts']
    except:
        parts_in = 0
    try:
        float(parts_out['parts'])
        parts_out = parts_out['parts']
    except:
        parts_out = 0

    total = parts_in - parts_out
    t = Part.objects.get(pk=self.Part_id)
    t.Quantity = int(total)
    t.save()

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
    Description = models.TextField(null=True, blank=True)
    def __unicode__(self):
        return self.Ordernr

    def save(self):
        super(PartChange, self).save()
        update_part(self)

    def delete(self):
        super(PartChange, self).delete()
        update_part(self)

    class Meta:
        ordering = ('Date',)
    
