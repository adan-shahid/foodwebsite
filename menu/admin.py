from django.contrib import admin
from .models import Category, foodItem



class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('category_name',)}
    list_display = ('category_name', 'vendor', 'updated_at')
    #SIMPL vendor  WILL NOT WORK, BCZ IT A FOREIGNKEY
    search_fields = ('category_name', 'vendor__vendor_name')


    

# Register your models here.
admin.site.register(Category,CategoryAdmin)
admin.site.register(foodItem)
