from django.contrib import admin

# Register your models here.
from authy.models import Team, Profile, Position

admin.site.register(Team)
admin.site.register(Profile)
admin.site.register(Position)

