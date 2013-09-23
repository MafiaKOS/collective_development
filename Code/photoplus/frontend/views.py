from django.http         import Http404
from django.shortcuts    import render_to_response
from django.template     import Context, loader, Template
from django.http         import HttpResponse
from apiclient.discovery import build
from frontend.models     import *
from sys                 import *
from math                import *
from django.core.mail 	 import send_mail
from django.template  	 import RequestContext
from django.http 	 import HttpResponseRedirect
from frontend.forms  	 import ReCaptchaForm
from frontend.forms  	 import buyForm
from frontend.models 	 import *
from django.core.mail 	 import EmailMultiAlternatives
from django.core.mail 	 import EmailMessage
from django.conf 	 import settings
from email.MIMEImage 	 import MIMEImage
from django 		 import template
from config             import ACCOUNT_EMAIL, ACCOUNT_PASSWORD, BEST_PHOTO_ALBUM
import gdata.photos.service
import gdata.media
import gdata.geo
import cgi
import datetime



import sys, traceback


LAST_VISIT_TO_ACCOUNT = 0







# Parsing tag info 

# in : string with hashtags
# out: list of tags( strings )

def get_tags_list( hashstring ):

    hashstring = hashstring.replace("&#","")
    tags_list = []
    for e in range( 0,hashstring.count("ot-hashtag") ):
        r = hashstring.find('#')+1
        hashstring = hashstring[r:]
        t = hashstring.find('<')
        tags_list.append( hashstring[:t] )
    return tags_list






# Extracting data from 
# personal account of Yuri Vashchenko

# in : ---
# out: list of structures like ---> [ url , [ #1_ht , #2_ht , ..

# ! Important: single use of this function spares 1 / 10.000 of API request !
def api_data_extraction():
    
    service = build(     'plus',
                         'v1', 
    developerKey =       'AIzaSyAKCO6eEQHQLN32ZARi2TOoJXVP88EZW4c')
    activities_resource = service.activities()
    request = activities_resource.list(
    userId =             '100915540970866628562',                                               #'103582189468795743999',
    collection =         'public',
    maxResults =         '100' )

    act_list = []
    activities_document = request.execute()
    if 'items' in activities_document:  
        for activity in activities_document['items']:                                           # taking every activity
            if 'actor' not in activity['object']:                                               # if activity is not reshared
                if 'attachments' in activity['object']:                                         # if activity has attachments
                    if activity['object']['attachments'][0]['objectType'] == "photo":           # if activity type is photo

                        act_struct = []                                                         # [ url , [ #1_ht , #2_ht , ... ] ]
                        act_struct.append( activity['object']['attachments'][0]['fullImage']['url'] ) 
                        act_struct.append( activity['updated'] )
                        act_struct.append( activity['url'] )
                        act_struct.append( strip_title( activity['object']['content'][:40] ) )
                        act_struct.append( get_tags_list( activity['object']['content'] ) )
                        
                        act_list.append( act_struct )

    return act_list

def refresh_db_with_new_data( ):
    
    new_data = api_data_extraction()
    posts_list = []
    
    for el in Post.objects.all():
        posts_list.append( el.image_url )
    
    for element in new_data:
        if element[0] not in posts_list:
            p = Post( image_url = element[0] , renew = element[1] , post_url = element[2] , post_title = element[3] )
            p.save()
        else:
            p = Post.objects.get( image_url = element[0] )
    
        if len(element) == 5:
            tags_list = []
            for el in Tag.objects.all():
                tags_list.append( el.name )
            for tag in element[4]:
                if tag not in tags_list:
                    t = Tag ( name = tag )
                    t.save()
                    t.posts.add(p)
                    t.save()
                else:
                    t = Tag.objects.filter( name = tag )[0]
                    t.posts.add(p)
                    t.save()
    return




def clear_db( ):

    p = Post.objects.all()
    t = Tag.objects.all()
    p.clear()
    t.clear()
    return

def contact(request):
            
    al = Album.objects.all()
    a = Author.objects.get(id=1)
    form = ReCaptchaForm()
    if request.POST:
        form = ReCaptchaForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            send_mail(
                cd['subject'],
                cd['message'],
                cd.get('email', a.email), [a.email], fail_silently=False
            	     )
            return HttpResponseRedirect('/about/')
    else:
        form = ReCaptchaForm(  )
    return render_to_response('contact.html', {'form': form, 'album_list':al}, context_instance=RequestContext(request))



def buy(request, idP, resolution):    
    try:
	al = Album.objects.all()
        a = Message.objects.get(id=1)
	pr = Price.objects.get( id = resolution)
        idP = int(idP)
        photo_id = Post.objects.get( id = idP )
    
    except Post.DoesNotExist:
        raise Http404
   
    t_to = Template(a.information_to) #to you
    t_from = Template(a.information_from) #from you/ means from admin
    s_to = Template(a.subject_to)
    s_from = Template(a.subject_from)

    codepage = request.get_host()
       
    form = buyForm()
    if request.POST:
        form = buyForm(request.POST)
        if form.is_valid():
    
            cd = form.cleaned_data
	    subject_to = a.subject_to
	    email_from = a.email
	    email_to = cd['Email']
	    country = cd['Country']
	    street1 = cd['Address1']
	    street2 = cd['Address2']
	    city = cd['City']
 	    state = cd['State']
	    zip_code = cd['Index']
	    f_name = cd['FirstName']
	    l_name = cd['LastName']
	    price = pr.price
	    size = str(pr.size) + u"*" + str(pr.on)
	    post_title = photo_id.post_title
	    image_url =  photo_id.image_url 
	    post_url =  photo_id.post_url 
 	   
	    order = Order(name= l_name + u" " + f_name,
			  adress = street1 + u", " + street2 + u", " + city + u", " + state + u", " + country + u", " + zip_code,
			  photo_id = image_url,
			  price = price,
			  size = size,
			  status = 'RECEIVED'
			)
            order.save()       
	    idorder = order.id
	    orderref = codepage + u'/order/' +   str(idorder) + u'/'
   
            c = Context({"f_name": f_name, "l_name": l_name, "country": country, "street1": street1, "street2": street2, "city":city, "state": state,  "zip_code": zip_code, "price": price, "size": size, "post_title":post_title, "image_url":image_url, "post_url": post_url, "orderref": orderref, "idorder": idorder })
	    
	    message_from = t_from.render(c)
	    subjectmessage_from = s_from.render(c)

	    message_to = t_to.render(c)
	    subjectmessage_to = s_to.render(c)
	
	    msg_from= EmailMessage(subjectmessage_from, message_from, email_from, [email_to]) 
	    msg_from.content_subtype = "html"  # Main content is now text/html
	   
	    msg_from.send()

	    msg_to = EmailMessage(subjectmessage_to, message_to, email_from, [email_from]) 
	    msg_to.content_subtype = "html"  # Main content is now text/html
	   
	    msg_to.send()
    
 #           send_mail(
 #               subject,
 #               messages,
 #               email_from, 
#		[email_to], 
#		fail_silently=False
 #          )
		

            return HttpResponseRedirect('/preview/' + str(idP))
    else:
        form = buyForm()
    return render_to_response('buy.html', {'form': form, 'buy':a, 'album_list':al }, context_instance=RequestContext(request))
 


#--------------------------------------------------------------------------------------------------
#                                          ABOUT
#--------------------------------------------------------------------------------------------------

def about(request):
    try:
        a = Author.objects.get(id=1)
        al = Album.objects.all()
    except Post.DoesNotExist:
        raise Http404
    return render_to_response('about.html',{ 'about':a , 'album_list':al })
#--------------------------------------------------------------------------------------------------
#                                          PREVIEW
#--------------------------------------------------------------------------------------------------
def preview(request, idP ):
    try:
        #album = Album.objects.get( name = idA)
        idP = int(idP)
        photo = Post.objects.get( id = idP )
        al = Album.objects.all()
        prices = Price.objects.all()
    except Post.DoesNotExist:
        raise Http404
    return render_to_response('preview.html',{ 'photo':photo , 'album':album, 'album_list':al, 'prices':prices })

def preview_best(request, photoId):
    try:
        photoId = int(photoId)
        photo = BestPhoto.objects.get( id = photoId )
        al = Album.objects.all()
        prices = Price.objects.all()
    except Post.DoesNotExist:
        raise Http404
    return render_to_response('preview.html',{ 'photo':photo , 'album':album, 'album_list':al, 'prices':prices })  

#--------------------------------------------------------------------------------------------------
#                                      GET_PAGINATOR_DATA
#--------------------------------------------------------------------------------------------------
def get_paginator_data( page, pages, adjacent_pages=2 ):
    startPage = max(page - adjacent_pages, 1)
    if startPage <= 3: startPage = 1
    endPage = page + adjacent_pages + 1
    if endPage >= pages - 1: endPage = pages + 1
    page_numbers = [n for n in range(startPage, endPage) \
            if n > 0 and n <= pages]
    if page != 1:
        has_previous = True
    else:
        has_previous = False
    if page != pages:
        has_next = True
    else:
        has_next = False
    if has_previous:
        previous_p = page - 1
    else:
        previous_p = 1
    if has_next:
        next_p = page + 1
    else:
        next_p = pages
    
    return {
        'page': page,
        'pages': pages,
        'page_numbers': page_numbers,
        'next': next_p,
        'previous': previous_p,
        'has_next': has_next,
        'has_previous': has_previous,
        'show_first': 1 not in page_numbers,
        'show_last': pages not in page_numbers,
    }
#--------------------------------------------------------------------------------------------------
#                                        STRIP_TITLE
#--------------------------------------------------------------------------------------------------
def strip_title( text ):
    if ( text.startswith("<b>") != True ):
        return ""
    pos = text.find("</b>")
    if (pos == -1):
        return ""
    title = text[3:pos]
    
    if ( (">" in title) or ("<" in title) or (len(title) > 30 ) ):
        return ""
    return title

#--------------------------------------------------------------------------------------------------
#                                       DESCRIBE_ALBUM
#--------------------------------------------------------------------------------------------------
def album( request , idA = "default", page = 1):
    
    page = int(page)
    
    if (page < 1):
        raise Http404
    try:
	album = Album.objects.get( name = idA)
	al = Album.objects.all()

	photos = []
	for tag in album.tags.all():
	    posts = tag.posts.all()
	    for post in posts:
		if post not in photos:
		    photos.append(post)
    except Album.DoesNotExist:
	raise Http404
    #    photos.sort(key=lambda post: post['id'])
		    
    num_last = 10 * page
    num_first = 10 * (page - 1)
		    
    pages = int(ceil(len(photos) / 10.0))
    paginator = get_paginator_data( page, pages , 2 )
    photos = photos[num_first:num_last]
		    
    num_first = num_first + 1
    num_last = num_first + len(photos) - 1
	    
    return render_to_response('albums.html',{'photos':photos, 'album':album , 'album_list':al, 'paginator':paginator, 'nl':num_last, 'nf':num_first})


#--------------------------------------------------------------------------------------------------

def home_page( request, page ):
    
    page = int(page)
    num_last = 10 * page
    num_first = 10 * (page - 1)
    
    try:
        last = Post.objects.order_by('-renew')[num_first:num_last]
        al = Album.objects.all()
    except Post.DoesNotExist:
        raise Http404
    
    num_first = num_first + 1
    num_last = num_first + len(last) - 1
    
    pages = int(ceil(Post.objects.count() / 10.0))
    paginator = get_paginator_data( page, pages , 2 )
    
    return render_to_response('index.html',{ 'last':last, 'paginator':paginator, 'nl':num_last, 'nf':num_first, 'album_list':al })

#-----------------------------------------------------------------------------------------------------

def home( request ):
    refresh_db_with_new_data()
    best_photo = get_best_photo()
    try:
        last = Post.objects.order_by('-renew')[0:10]
        al = Album.objects.all()
    except Post.DoesNotExist:
        raise Http404
   # if len(best_photo) == 0:
   #     raise Http404
    
    page = 1
    pages = int(ceil(Post.objects.count() / 10.0))
    paginator = get_paginator_data( page, pages , 2 )
    num_last = len(last)
    #raise Exception, "url : %s" % best_photo[0]
    return render_to_response('index.html',{ 'last':last, 'best_photo':best_photo,'best':last[:3], 'paginator':paginator, 'nl':num_last, 'nf':1, 'album_list':al })
#'best_photo':best_photo,


def change_albums_name(album_name):
    album_name.strip()
    album_name.replace(' ', '-')
    return album_name


def order(request, idOrder):
    try:
	al = Album.objects.all()
        orderlast = Order.objects.get(id=idOrder)
        ordersall = Order.objects.filter(name=orderlast.name, adress = orderlast.adress)

    except Post.DoesNotExist:
        raise Http404
    return render_to_response('order.html',{ 'ordersall':ordersall , 'orderlast':orderlast, 'album_list':al })

def get_best_photo():
    now = datetime.datetime.now()
    # retrive date time of last visit to account
    
    if len(LastUpdated.objects.all()) == 0:
        last_update = LastUpdated(last_visit = now, album_update = "")
        last_update.save()
    
    last_update = LastUpdated.objects.get(id=1)
    local_last_visit = last_update.last_visit

    
    photos_from_db = []
   
    # get photos from db
    for el in BestPhoto.objects.all():
        photos_from_db.append( el.image_url )
    
    if len(photos_from_db) == 0 or abs(local_last_visit.hour - now.hour) >= 3 or abs(local_last_visit.day - now.day) >= 1:
        # update last visit in db        
        last_update.last_visit = now
        last_update.save()
        photos_from_db = update_best_photos()
   
    return photos_from_db
    
def update_best_photos():
    gd_client = gdata.photos.service.PhotosService()
    gd_client.email = ACCOUNT_EMAIL
    gd_client.password = ACCOUNT_PASSWORD
    gd_client.ProgrammaticLogin()
    photos_from_account = []
    photos_from_db=[]

    # retrive datetime (type is string )of last visit to account
    last_update = LastUpdated.objects.get(id=1)
    local_album_update = last_update.album_update

    update_date = 0 # best photos album's update time 
    act_list = []
    #last_update = 0 # best photos album's update time. It is taked from last photo info from db

    # get photos from db
   
      
    albums = gd_client.GetUserFeed()
    
    for el in BestPhoto.objects.all():
        photos_from_db.append( el.image_url ) 

    # get photos from account
    for album in albums.entry:
        if album.title.text == BEST_PHOTO_ALBUM:
            # if album has updated
            #raise Exception, "update.text: %s , album_update: %s" %(album.updated.text,local_album_update)
            if album.updated.text != local_album_update:
                #update the album_update value in db
                last_update.album_update = album.updated.text
                last_update.save()
                
                photos = gd_client.GetFeed('/data/feed/api/user/%s/albumid/%s?kind=photo' % ('default', album.gphoto_id.text)) 
                #get all photos from account
                for photo in photos.entry:
                    photos_from_account.append(photo.content.src)
                    #raise Exception, "src is %s" %len(photo.content.src)
                for el in BestPhoto.objects.all():
                    if el.image_url not in photos_from_account:
                        el.delete() 
  
    # compaire photos from account and db: if the photo from account is absent indb, then the photo is added into db
    for element in photos_from_account:
        if element not in photos_from_db:
            p = BestPhoto( image_url = element)
            p.save()

    photos_from_db = []

   # raise Exception, "length db is %d" %len(BestPhoto.objects.all()) 
    for el in BestPhoto.objects.all():
       # photos_from_db.append( el.image_url )  
	    photos_from_db.append( el ) 
       # raise Exception, "url %s" % el.image_url
    
    return photos_from_db 


