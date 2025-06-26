from django.contrib import admin
from .models import CustomUser
#
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['view','name_firma','inn','kPP','Address','email','director']



admin.site.register(CustomUser)


# Register your models here.
