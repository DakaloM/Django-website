from django.contrib import admin
from .models import Venue
from .models import MyClubUser
from .models import Event
from django.contrib.auth.models import User # import user model from django
# Register your models here.


#admin.site.register(Venue)
admin.site.register(MyClubUser)
#admin.site.register(Event)

# To make changes in the admin area
@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
	list_display = ('name', 'address', 'phone', 'zip_code', 'web', 'email_address')
	ordering = ('name',)
	search_fields = ('name', 'address')

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
	fields = (('id','name', 'venue'), 'event_date', 'description', 'manager')
	list_display = ('id','name', 'event_date', 'venue', 'manager', 'description')
	list_filter = ('event_date', 'venue')
	ordering = ('id',)
 

