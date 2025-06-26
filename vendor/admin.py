from django.contrib import admin

from .models import Vendor

#IN THE VENDOR MODEL'S ADMIN PANEL, ONLY VENDOR NAME IS SHOWING. NO OTHER FIELD IS SHOWING.
#TO SHOW OTHER FIELDS, WE ARE WRITING THIS LOGIC

class VendorAdmin(admin.ModelAdmin):
    list_display = ('user', 'vendor_name','is_approved', 'created_at')
    list_display_links = ('user', 'vendor_name')
    list_editable = ('is_approved',)

admin.site.register(Vendor, VendorAdmin)