from pmdb.models import Part
from pmdb.models import Housing
from pmdb.models import Manufacturer
from pmdb.models import Category 
from pmdb.models import Unit

from django.contrib import admin

class PartAdmin(admin.ModelAdmin):
    list_display = ('Model', 'Quantity', 'Housing', 'Manufacture')
    search_fields = ['Model']
    fieldsets = [
        (None,          {'fields': ['Model','Quantity','Description','Category']}),
        ('Details',     {'fields': ['Manufacture','Housing','Amount','Unit','Datasheet']}),
    ]

class HousingAdmin(admin.ModelAdmin):
    list_display = ['Housing']
    ordering = ['Housing']

admin.site.register(Part, PartAdmin)
admin.site.register(Manufacturer)
admin.site.register(Category)
admin.site.register(Unit)
admin.site.register(Housing, HousingAdmin)

