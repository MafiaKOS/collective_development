from django.contrib import admin
from frontend.models import *



class AlbumAdmin(admin.ModelAdmin):
    pass
admin.site.register(Album, AlbumAdmin)

class MessageAdmin(admin.ModelAdmin):
    pass
admin.site.register(Message, MessageAdmin)


class AuthorAdmin(admin.ModelAdmin):
	pass	
admin.site.register(Author, AuthorAdmin)

class PriceAdmin(admin.ModelAdmin):
	pass	
fields = ('price', ('size', 'on'))
admin.site.register(Price, PriceAdmin)

