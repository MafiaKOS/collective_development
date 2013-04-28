


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

	name = models.CharField( max_length=200 )
	tags = models.ManyToManyField( Tag )

	def __unicode__( self ):
		return self.name





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

	email = models.EmailField( max_length=200 )
	subject = models.CharField( max_length=200)
	information = models.TextField(max_length=10000)
 
class Price ( models.Model ):
	price = models.PositiveSmallIntegerField(max_length=4, default=0)
	size = models.PositiveSmallIntegerField( max_length=10, default=10 )
 	on = models.PositiveSmallIntegerField( max_length=10, default=10 )
	 	
