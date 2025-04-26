from django.contrib import admin
from django.contrib import admin
from .models import Client, HealthProgram, Enrollment

# Register your models here.

# Register the HealthProgram model
class HealthProgramAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

admin.site.register(HealthProgram, HealthProgramAdmin)

# Register the Client model
class ClientAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'national_id', 'date_of_birth', 'contact')
    search_fields = ('full_name', 'national_id')

admin.site.register(Client, ClientAdmin)

# Register the Enrollment model
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('client', 'program', 'date_enrolled')
    list_filter = ('program',)
    search_fields = ('client__full_name', 'program__name')

admin.site.register(Enrollment, EnrollmentAdmin)
