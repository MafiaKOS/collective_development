


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


# Contains information about messages

class Message ( models.Model ):
    
    name = models.CharField( max_length=200 )
    text = models.CharField( max_length=500 )

    def __unicode__( self ):
        return self.name


class Price( models.Model ):

    size = models.CharField( max_length=200 )
    price = models.IntegerField()

    def __unicode__( self ):
        return self.size

class Author( models.Model ):

    photo_url = models.CharField( max_length=200 )
    information = models.CharField(max_length=10000)
    email = models.CharField( max_length=200)

    def __unicode__( self ):
        return self.email
