


from django.db import models





# Contains information about single activity unit ( photo )

class Post ( models.Model ):

	post_title = models.CharField( max_length=35 )
    	renew = models.DateTimeField( 'date of renewal' )
   	image_url = models.CharField( max_length=200 )
    	post_url = models.CharField( max_length=200 )



# Contains information about a tag

class Tag ( models.Model ):

	name = models.CharField( max_length=200 )
	posts = models.ManyToManyField( Post )

	def __unicode__( self ):
		return self.name




# Contains information about an album

class Album ( models.Model ):

	name = models.SlugField( max_length=200 )
	tags = models.ManyToManyField( Tag )

	def __unicode__( self ):
		return self.name
	
	def save(self):
        	self.name = self.name.strip()
		self.name = self.name.replace(' ', '_')
		self.name = self.name.replace('-', '_')
        	super(Album, self).save() 

# Contains admin security data

class Admin ( models.Model ):

	login = models.CharField( max_length=200 )
	hashpass = models.CharField( max_length=200 )
	renew = models.DateTimeField( 'date of total renewal' )

class Author( models.Model ):

	photo_url = models.CharField( max_length=200 )
	information = models.TextField(max_length=10000)
	email = models.EmailField()

class Message( models.Model ):

	email = models.EmailField( max_length=200, verbose_name="From", help_text="Address to which and from which comes an order to commit" )
	subject_from = models.CharField( max_length=200)
	information_from = models.TextField(max_length=10000, help_text="You can use the following templates: <br> {{f_name}} - first buyer's name, {{l_name}} - last buyer's name, {{country}}, {{street1}}, {{street2}}, {{city}}, {{state}} - buyer's address, <br> {{zip_code}} - zip code, {{price}} - price of purchased photos, {{size}} - size of purchased photos, {{post_title}} - header photos, <br> {{image_url}} - URL of photos in G+, {{post_url}} - URL of post in G+, {{orderref}} - link to order, {{idorder}} - order number" )
	subject_to = models.CharField( max_length=200)
	information_to = models.TextField(max_length=10000, help_text="You can use the following templates: <br> {{f_name}} - first buyer's name, {{l_name}} - last buyer's name, {{country}}, {{street1}}, {{street2}}, {{city}}, {{state}} - buyer's address, <br> {{zip_code}} - zip code, {{price}} - price of purchased photos, {{size}} - size of purchased photos, {{post_title}} - header photos, <br> {{image_url}} - URL of photos in G+, {{post_url}} - URL of post in G+, {{orderref}} - link to order, {{idorder}} - order number" )
	
 
class Price ( models.Model ):
	price = models.PositiveSmallIntegerField(max_length=4, default=0)
	size = models.PositiveSmallIntegerField( max_length=10, default=10 )
 	on = models.PositiveSmallIntegerField( max_length=10, default=10 )

class Order ( models.Model ):
	Order_choices = (
	    ('RECEIVED ', 'RECEIVED '),
	    ('SHIPPED  ', 'SHIPPED  '),
	    ('ORDER PROCESSING', 'ORDER PROCESSING'),
	    ('CANCELLED', 'CANCELLED'),
	)
	name = models.CharField( max_length=150, help_text="The buyer's name")
	adress = models.CharField( max_length=400, help_text="The buyer's address")
 	photo_id = models.CharField( max_length=200, verbose_name="photo URL")
	price = models.PositiveSmallIntegerField(max_length=4, default=0)
	size = models.CharField( max_length=22)
	status = models.CharField(max_length=20,choices=Order_choices, default='RECEIVED')

class BestPhoto (models.Model):
    image_url = models.CharField( max_length = 400 )

class LastUpdated (models.Model):
    last_visit = models.DateTimeField()
    album_update = models.CharField( max_length = 400 )
	
