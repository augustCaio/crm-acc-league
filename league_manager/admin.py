from django.contrib import admin
from .models import Team, Driver, Event, RaceResult

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'team', 'nationality')
    search_fields = ('full_name', 'nickname', 'team__name')
    list_filter = ('team', 'nationality')

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'track_name', 'event_date')
    search_fields = ('name', 'track_name')
    list_filter = ('event_date',)

@admin.register(RaceResult)
class RaceResultAdmin(admin.ModelAdmin):
    list_display = ('event', 'driver', 'final_position', 'points_earned')
    search_fields = ('event__name', 'driver__full_name')
    list_filter = ('event', 'driver__team')
    autocomplete_fields = ['event', 'driver', 'team']
