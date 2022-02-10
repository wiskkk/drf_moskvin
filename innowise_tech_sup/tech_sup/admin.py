from django.contrib import admin

from .models import Answer, Ticket

admin.site.register(Ticket)
admin.site.register(Answer)
