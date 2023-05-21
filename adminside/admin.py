from django.contrib import admin
from .models import Message, ReplyOnMessage

# Register your models here.
admin.site.register(Message)
admin.site.register(ReplyOnMessage)