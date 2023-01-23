from django.contrib import admin

# Register your models here.
from app.models import Note, Achievement, Ad, User

admin.site.register(Note)
admin.site.register(Achievement)
admin.site.register(Ad)
admin.site.register(User)
