from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Company, Faq, Package, Customer, Space, Booking, Contact, PackageDetails, CleanUp

class CustomerInline(admin.StackedInline):
    model = Customer
    can_delete = False

class UserAdmin(BaseUserAdmin):
    inlines = (CustomerInline,)

# Register your models here.
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Company)
admin.site.register(Faq)
admin.site.register(Package)
admin.site.register(Space)
admin.site.register(Booking)
admin.site.register(PackageDetails)
admin.site.register(CleanUp)
admin.site.register(Contact)
