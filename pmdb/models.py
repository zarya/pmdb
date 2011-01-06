from django.db import models

# Create your models here.

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

class Part(models.Model):
    Model = models.CharField(max_length=200)
    Housing = models.ForeignKey(Housing)
    Category = models.ManyToManyField(Category)
    Manufacture = models.ForeignKey(Manufacturer)
    Quantity = models.CharField(max_length=30)
    Description = models.TextField()
    Unit = models.ForeignKey(Unit,null=True, blank=True)
    Amount = models.CharField(max_length=10,null=True,blank=True)
