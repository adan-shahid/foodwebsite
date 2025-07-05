from django.contrib import admin
from .models import Category, foodItems


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('category_name',)}

# Register your models here.
admin.site.register(Category,CategoryAdmin)
admin.site.register(foodItems)
