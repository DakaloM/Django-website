from django.db import models
from django.contrib.auth.models import User
# Create your models here.
# each class represent a table
 
class Venue(models.Model):
	name = models.CharField('Venue Name', max_length=200)
	address =models.CharField(max_length=200)
	zip_code = models.CharField('Zip Code', max_length=200)
	phone = models.CharField('Contact Number', max_length=50, blank=True)
	web = models.URLField('Website Address', blank=True)
	email_address = models.EmailField("Email Address", blank=True)
	owner = models.IntegerField("Owner", blank=False, default=1)
	venue_image = models.ImageField(null=True, blank=True, upload_to="image/")

	def __str__(self):
 		return self.name 


class MyClubUser(models.Model):
	first_name = models.CharField(max_length=225)
	last_name = models.CharField(max_length=225)
	email = models.EmailField('User Email')

	def __str__(self):
 		return self.first_name + " " + self.last_name

class Event(models.Model): 

 	#defining the table columns
 	name = models.CharField('Event Name', max_length=225)
 	event_date = models.DateTimeField('Event Date')
 	venue = models.ForeignKey(Venue, blank=True, null=True, on_delete = models.CASCADE) # Linking Event and Venue tables
 	#venue = models.CharField( max_length=225)
 	manager =models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
 	description =  models.TextField(blank = True)
 	
 	attendees = models.ManyToManyField(MyClubUser, blank=True) #many to many relationship


 	def __str__(self):
 		return self.name
