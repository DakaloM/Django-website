from django import forms
from django.forms import ModelForm
from .models import Venue, Event

# Create Event Form Admin
class EventFormAdmin(ModelForm):
	

	class Meta:
		model = Event
		fields = ('name', 'event_date','venue','manager','description', 'attendees')

		#Adding some styling

		labels = {

			'name':'Name' ,
			'event_date': 'Date:  (YYYY-MM-DD HH:MM)' ,
			'venue': 'Venue',
			'manager': 'Manager',
			'description': 'Description',
			'attendees': 'Attendees',
		}

		widgets = {
			'name': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Event Name'}),
			'event_date':forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Event Date'}),
			'venue':forms.Select(attrs={'class':'form-select', 'placeholder': 'Venue'}),
			'manager':forms.Select(attrs={'class':'form-select', 'placeholder': 'Manager'}),
			'description':forms.Textarea(attrs={'class':'form-control', 'placeholder': 'Description'}),
			'attendees':forms.SelectMultiple(attrs={'class':'form-control', 'placeholder': 'Attendees'}),
		}

# Form for regular users
class EventForm(ModelForm):
	

	class Meta:
		model = Event
		fields = ('name', 'event_date','venue','description', 'attendees')

		#Adding some styling

		labels = {

			'name':'Name' ,
			'event_date': 'Date:  (YYYY-MM-DD HH:MM)' ,
			'venue': 'Venue',
			'description': 'Description',
			'attendees': 'Attendees',
		}

		widgets = {
			'name': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Event Name'}),
			'event_date':forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Event Date'}),
			'venue':forms.Select(attrs={'class':'form-select', 'placeholder': 'Venue'}),
			'description':forms.Textarea(attrs={'class':'form-control', 'placeholder': 'Description'}),
			'attendees':forms.SelectMultiple(attrs={'class':'form-control', 'placeholder': 'Attendees'}),
		}
	
# Create a venue form
class VenueForm(ModelForm):
	class Meta:
		model = Venue
		fields = ('name', 'address', 'zip_code', 'phone', 'web', 'email_address' ,'venue_image')

		# Adding styling to the form

		labels = {

			'name':'' ,
			'address': '',
			'zip_code': '',
			'phone': '',
			'web': '',
			'email_address': '',
			'venue_image': ''
		}

		widgets = {
			'name': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Enter the Venue Name'}),
			'address':forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Address'}),
			'zip_code':forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Zip Code'}),
			'phone':forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Contact Number'}),
			'web':forms.URLInput(attrs={'class':'form-control', 'placeholder': 'Website Url'}),
			'email_address':forms.EmailInput(attrs={'class':'form-control', 'placeholder': 'Email Address'}),
		}