from django.contrib import admin
from frontend.models import *



class AlbumAdmin(admin.ModelAdmin):
    pass
admin.site.register(Album, AlbumAdmin)

class MessageAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,		{'fields': ['email']}),
	('Message to you', 	{'fields': ['subject_to', 'information_to']}),
        ('Message from you', 	{'fields': ['subject_from', 'information_from']}),
	]

admin.site.register(Message, MessageAdmin)


class AuthorAdmin(admin.ModelAdmin):
	pass	
admin.site.register(Author, AuthorAdmin)

class PriceAdmin(admin.ModelAdmin):
	pass	
fields = ('price', ('size', 'on'))
admin.site.register(Price, PriceAdmin)

class OrderAdmin(admin.ModelAdmin):	
    list_display = ('name', 'adress', 'photo_id', 'price', 'size', 'status')
    list_editable = ['status']
    list_filter = ['status']
    readonly_fields = ('name', 'adress', 'photo_id', 'price', 'size',)
admin.site.register(Order, OrderAdmin)

