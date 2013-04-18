


from django.contrib 				import admin
from frontend.models 				import *
from django.contrib.auth.models 	import User, Group
from django.contrib.sites.models 	import Site

admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.unregister(Site)



class AlbumAdmin(admin.ModelAdmin):
    pass

class MessageAdmin(admin.ModelAdmin):
	pass
	
class PriceAdmin(admin.ModelAdmin):
	pass	

class AuthorAdmin(admin.ModelAdmin):
	pass	


admin.site.register(Album, AlbumAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Price, PriceAdmin)
admin.site.register(Author, AuthorAdmin)