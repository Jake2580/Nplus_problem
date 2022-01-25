from django.contrib import admin

from reservations.models import Owner, Reservation

# Register your models here.
admin.site.register(Reservation)
admin.site.register(Owner)
