from django.contrib import admin
from .models import Appointment

# Register your models here.


@admin.register(Appointment)
class appointmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'submitted_at')
    search_fields = ('name', 'email', 'phone')
    list_filter = ('submitted_at',)
