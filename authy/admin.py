from django.contrib import admin

# Register your models here.
from authy.models import Team, Profile, Position, TeamManager

admin.site.register(Team)
admin.site.register(Profile)
admin.site.register(Position)
admin.site.register(TeamManager)
