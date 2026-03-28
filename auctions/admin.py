from django.contrib import admin
from.models import User, Listing,category
# customized the admin pannel 
class ListingAdmin(admin.ModelAdmin):
    list_display =("id" , "Name","cover","Starting_Bid", "Description","isActive","category","Lister",)

# Register your models here.
admin.site.register(Listing,ListingAdmin)
admin.site.register(User)
admin.site.register(category)

