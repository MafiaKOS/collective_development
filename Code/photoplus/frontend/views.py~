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
        form = ReCaptchaForm(  initial={'subject': 'I love your site!'}
			     )
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
   
    t = Template(a.information)
    s = Template(a.subject)
       
    form = buyForm()
    if request.POST:
        form = buyForm(request.POST)
        if form.is_valid():
    
            cd = form.cleaned_data
	    subject = a.subject
	    email_from = a.email
	    email_to = cd['Email']
	    country = cd['Country']
	    adress = cd['Adress']
	    index = cd['Index']
	    f_name = cd['FirstName']
	    l_name = cd['LastName']
	    price = pr.price
	    size = str(pr.size) + u"*" + str(pr.on)
	    post_title = photo_id.post_title
	    image_url =  photo_id.image_url 
	    post_url =  photo_id.post_url 
 	   
	    order = Order(name= l_name + u" " + f_name,
			  adress = country + u", " + adress + u", " + index,
			  photo_id = image_url,
			  price = price,
			  size = size,
			  status = 'RECEIVED'
			)
            order.save()       
	    idorder = order.id
	    orderref = u'loc.vashchenko.com/order/' +   str(idorder) + u'/'
   
            c = Context({"f_name": f_name, "l_name": l_name, "country": country, "adress": adress, "index": index, "price": price, "size": size, "post_title":post_title, "image_url":image_url, "post_url": post_url, "orderref": orderref, "idorder": idorder })
	    messages = t.render(c)
	    subjectmessages = s.render(c)
	    
	    
	    html_content = t.render(c) 
	    msg = EmailMessage(subject, html_content, email_from, [email_to]) 
	    msg.content_subtype = "html"  # Main content is now text/html
	   
	    msg.send()
    
 #           send_mail(
 #               subject,
 #               messages,
 #               email_from, 
#		[email_to], 
#		fail_silently=False
 #          )
		

            return HttpResponseRedirect('/about/')
    else:
        form = buyForm( # initial={'subject': 'I love your site!'}
			     )
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
    try:
        last = Post.objects.order_by('-renew')[0:10]
        al = Album.objects.all()
    except Post.DoesNotExist:
        raise Http404
    
    page = 1
    pages = int(ceil(Post.objects.count() / 10.0))
    paginator = get_paginator_data( page, pages , 2 )
    num_last = len(last)
    
    return render_to_response('index.html',{ 'last':last, 'best':last[:3], 'paginator':paginator, 'nl':num_last, 'nf':1, 'album_list':al })


def order(request, idOrder):
    try:
	al = Album.objects.all()
        orderlast = Order.objects.get(id=idOrder)
        ordersall = Order.objects.filter(name=orderlast.name, adress = orderlast.adress)

    except Post.DoesNotExist:
        raise Http404
    return render_to_response('order.html',{ 'ordersall':ordersall , 'orderlast':orderlast, 'album_list':al })
 


