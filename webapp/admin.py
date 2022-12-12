from django.contrib import admin
from .models import UserMaster,ImageMaster,LikeMaster

# Register your models here.

ModelField= lambda model: type('Subclass'+model.__name__,(admin.ModelAdmin,),{
    'list_display':[x.name for x in model._meta.fields],    
})

admin.site.register(UserMaster,ModelField(UserMaster))
admin.site.register(ImageMaster,ModelField(ImageMaster))
admin.site.register(LikeMaster,ModelField(LikeMaster))
