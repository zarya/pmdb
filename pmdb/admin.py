from pmdb.models import Part
from pmdb.models import Housing
from pmdb.models import Manufacturer
from pmdb.models import Category 
from pmdb.models import Unit
from pmdb.models import Project 
from pmdb.models import PartChange 

from django.contrib import admin

class PartChange(admin.TabularInline):
    model = PartChange
    extra = 1
    ordering = ['Date']
    can_delete = True
    fieldsets = [ 
        (None, {'fields': ['Direction','Quantity', 'Project']}),
        (None, {'fields': ['Supplier','Ordernr', 'Description']}),
    ]

class PartAdmin(admin.ModelAdmin):
    list_display = ('Model', 'Quantity', 'Housing', 'Manufacture')
    search_fields = ['Model']
    fieldsets = [
        (None,          {'fields': ['Model','Quantity','Description','Category']}),
        ('Details',     {'fields': ['Manufacture','Housing','Amount','Unit','Datasheet']}),
    ]
    readonly_fields = [ 'Quantity' ]
    inlines = [
        PartChange
    ]

class HousingAdmin(admin.ModelAdmin):
    list_display = ['Housing']
    ordering = ['Housing']

class ProjectAdmin(admin.ModelAdmin):
    list_display = ['Name','get_part_list']
    inlines = [
        PartChange
    ]

admin.site.register(Part, PartAdmin)
admin.site.register(Manufacturer)
admin.site.register(Category)
admin.site.register(Unit)
admin.site.register(Housing, HousingAdmin)
admin.site.register(Project, ProjectAdmin)
