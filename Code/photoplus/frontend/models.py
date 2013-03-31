


from django.db import models





# Contains information about single activity unit ( photo )

class Post ( models.Model ):

	image_url = models.CharField( max_length=200 )
	post_url = models.CharField( max_length=200 )
	renew = models.DateTimeField( 'date of renewal' )



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