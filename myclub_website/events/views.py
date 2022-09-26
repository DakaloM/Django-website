from django.shortcuts import render, redirect
import calendar
from django.http import HttpResponseRedirect
from calendar import HTMLCalendar
from datetime import datetime
from .models import Event, Venue
from django.contrib.auth.models import User # import user model from django
from .forms import VenueForm, EventForm, EventFormAdmin
from django.http import HttpResponse
import csv
from django.contrib import messages
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

# Import pagination stuff

from django.core.paginator import Paginator

# Create your views here.
def search_events(request):
	if request.method == "POST":
		search = request.POST['search']
		venues = Venue.objects.filter(name__contains=search)
		return render(request, 'events/search_venues.html', {'search': search, 'venues': venues})



	else:
		return render(request, 'events/search_venues.html', {})

#My events function
def my_events(request):
	if request.user.is_authenticated:
		me = request.user.id
		event_list = Event.objects.filter(attendees=me)
		return render(request, 'events/my_events.html', {'event_list': event_list})
	else:
		messages.success(request, ("Error, You are not authorised to access this page"))
		return redirect('home')

# getting all events from the database
def all_events(request):
	event_list = Event.objects.all().order_by('name')
	return render(request, 'events/event_list.html', {'event_list': event_list})
#___________________________________________________________________________________________


# Add Event
def add_event(request):
	submitted = False
	if request.method == "POST":
		if request.user.is_superuser:
			form = EventFormAdmin(request.POST)
			if form.is_valid():
				form.save()
				return HttpResponseRedirect('/add_event?submitted=True') #submitted into the Get request

		else:
			form = EventForm(request.POST)
			if form.is_valid():
				event = form.save(commit=False)
				event.manager = request.user
				event.save()
				return HttpResponseRedirect('/add_event?submitted=True') #submitted into the Get request

	else:
		# just going to the page, not submitting
		if request.user.is_superuser:
			form = EventFormAdmin

		else:
			form = EventForm
		if 'submitted' in request.GET:
			submitted = True

	return render(request, 'events/add_event.html', {'form': form, 'submitted': submitted})



# Delete an event
def delete_event(request, event_id):
	event = Event.objects.get(pk=event_id)
	if request.user == event.manager or request.user.is_superuser:
		event.delete()
		messages.success(request, ("Event Deleted"))
		return redirect('list-events')
	else:
		messages.success(request, ("Error, You are not authorised to delete this event"))
		return redirect('list-events')
#_____________________________________________________________________________________________________________________________________

# Update Event info
def update_event(request, event_id):
	event = Event.objects.get(pk=event_id)
	if request.user.is_superuser:
		form = EventFormAdmin(request.POST or None, instance=event)
		
	else:
		form = EventForm(request.POST or None, instance=event)
		
	if form.is_valid():
		form.save()
		return redirect('list-events')

	return render(request, 'events/update_event.html', {'event': event, 'form': form})


# Update Venue info
def update_venue(request, venue_id):
	venue = Venue.objects.get(pk = venue_id) #get data for specific id(primary key)
	form = VenueForm(request.POST or None, instance = venue)
	if form.is_valid():
		form.save()
		return redirect('list-venues')

	return render(request, 'events/update_venue.html', {'venue': venue, 'form': form})
#____________________________________________________________________________________________________________________________________________


# Generate PDF file
def venue_pdf(response):

	#create Bytestream buffer
	buf = io.BytesIO()

	# Create Canvas
	c = canvas.Canvas(buf, pagesize=letter, bottomup=0)

	# Create a text object
	textob = c.beginText()
	textob.setTextOrigin(inch, inch)
	textob.setFont("Helvetica", 14)

	# Get all Venues from the model
	venues = Venue.objects.all()

	# Create a blank list
	lines = []

	# Loop though all the lines
	for venue in venues:
		lines.append(venue.name)
		lines.append(venue.address)
		lines.append(venue.zip_code)
		lines.append(venue.phone)
		lines.append(venue.web)
		lines.append(venue.email_address)
		lines.append(" ")


	for line in lines:
		textob.textLine(line)

	# Finishing up
	c.drawText(textob)
	c.showPage()
	c.save()
	buf.seek(0)

	# Return something
	return FileResponse(buf, as_attachment=True, filename='venues.pdf')

#Generate a CSV File
def venue_csv(request):
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename=venues.csv'

	# Create a CSV Writer
	writer = csv.writer(response)

	# Get all Venues 
	venues = Venue.objects.all()

	# Add column headings to the csv file
	writer.writerow(['Name', 'Address', 'Zip Code','Contact','Website', 'Email' ])

	for venue in venues:
		writer.writerow([venue.name, venue.address, venue.zip_code, venue.phone, venue.web, venue.email_address])




	return response

#____________________________________________________________________________________________________________________________________________

# Generating Text Files
def venue_text(request):
	response = HttpResponse(content_type='text/plain')
	response['Content-Disposition'] = 'attachment; filename=venues.txt'

	venues_list = []

	# Get all Venues info
	venues = Venue.objects.all()
	for venue in venues:
		venues_list.append(f"{venue.name} \n {venue.address}\n {venue.zip_code}\n {venue.phone}\n {venue.web}\n {venue.email_address}\n\n")


	#write to txt file
	response.writelines(venues_list)
	return response

#_________________________________________________________________________________________________________________________________________
# Delete Venue
def delete_venue(request, venue_id):
	venue = Venue.objects.get(pk=venue_id)
	if request.user.id == venue.owner or request.user.is_superuser:
		venue.delete()
		messages.success(request, ("Venue Deleted"))
		return redirect('list-venues')
	else:
		messages.success(request, ("Error!, You are not authorised to delete this Venue"))
		return redirect('list-venues')

# Search for a specific venue
def search_venues(request):
	if request.method == "POST":
		search = request.POST['search']
		venues = Venue.objects.filter(name__contains=search)
		return render(request, 'events/search_venues.html', {'search': search, 'venues': venues})

	else:
		return render(request, 'events/search_venues.html', {})
#_________________________________________________________________________________________________

# Display venues from the database	
def show_venue(request, venue_id):
	venue = Venue.objects.get(pk = venue_id) #get data for specific id(primary key)
	venue_owner = User.objects.get(pk=venue.owner)
	return render(request, 'events/show_venue.html', {'venue': venue, 'venue_owner': venue_owner})


def list_venues(request):
	venue_list = Venue.objects.all().order_by('name')

	# Set up Pagination
	p = Paginator(venue_list, 4)
	page = request.GET.get('page')
	venues = p.get_page(page)
	nums = "a" * venues.paginator.num_pages
	return render(request, 'events/venues.html', {'venue_list': venue_list, 'venues': venues, 'nums' :nums})
#________________________________________________________________________________________________________

def add_venue(request):

	submitted = False
	if request.method == "POST":
		form = VenueForm(request.POST, request.FILES)
		if form.is_valid():
			venue = form.save(commit=False)
			venue.owner = request.user.id
			venue.save()
			return HttpResponseRedirect('/add_venue?submitted=True') #submitted into the Get request
	else:
		form = VenueForm
		if 'submitted' in request.GET: # check if the submitted is in the Get request
			submitted = True

	return render(request, 'events/add_venue.html', {'form':form, 'submitted': submitted})



def home(request, year=datetime.now().year, month=datetime.now().strftime('%B')):
	name = "Dakalo"
	month = month.capitalize()

	#convert month from string top int
	month_number = list(calendar.month_name).index(month)
	#make sure this number is int
	month_number = int(month_number)

	#create a calendar
	cal = HTMLCalendar().formatmonth(year, month_number)

	#get current year
	now = datetime.now()
	current_year = now.year

	#get the current time
	time = now.strftime('%H:%M,%S')

	return render(request,
		 'events/home.html',
		  {
		  	"name" : name,
		  	"year" : year,
		  	"month": month,
		  	"month_number": month_number,
		  	"cal":cal,
		  	"current_year": current_year,
		  	"time": time
		  })