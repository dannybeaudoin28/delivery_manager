from django.contrib import admin
from .models import Driver, Route, Delivery

admin.site.register(Driver)
admin.site.register(Route)
admin.site.register(Delivery)