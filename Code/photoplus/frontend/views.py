# coding=UTF-8


from django.http         import Http404
from django.shortcuts    import render_to_response
from django.template     import Context, loader
from django.http         import HttpResponse

from apiclient.discovery import build
from frontend.models     import *
from sys                 import *
from math                import *




# Parsing tag info 

# in : string with hashtags
# out: list of tags( strings )

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

def get_tags_list( hashstring ):

    hashstring = hashstring.replace("&#","")
    tags_list = []
    for e in range( 0,hashstring.count("ot-hashtag") ):
        r = hashstring.find('#')+1
        hashstring = hashstring[r:]
        t = hashstring.find('<')
        tags_list.append( hashstring[:t] )
    return tags_list


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
    if 'items' in activities_document:                                                          # if account is not empty
        for activity in activities_document['items']:                                           # taking every activity
            if 'actor' not in activity['object']:                                               # if activity is not reshared
                if 'attachments' in activity['object']:                                         # if activity has attachments
                    if activity['object']['attachments'][0]['objectType'] == "photo":           # if activity type is photo
    
                        act_struct = []                                                         # [ url , [ #1_ht , #2_ht , ... ] ]
                        act_struct.append( activity['object']['attachments'][0]['fullImage']['url'] ) 
                        act_struct.append( activity['updated'] )
                        act_struct.append( get_tags_list( activity['object']['content'] ) )
                        act_struct.append( activity['url'] )
                        act_struct.append( strip_title( activity['object']['content'][:40] ) )
                        
                        act_list.append( act_struct )
    return act_list





def refresh_db_with_new_data( ):
    
    new_data = api_data_extraction()
    
    posts_list = []
    for el in Post.objects.all():
        posts_list.append( el.image_url )
    
    for element in new_data:
        if element[0] not in posts_list:
            p = Post( image_url = element[0] , renew = element[1] , post_url = element[3] , post_title = element[4])
            p.save()
        else:
            p = Post.objects.get( image_url = element[0] )
    
        if len(element) == 3:
            tags_list = []
            for el in Tag.objects.all():
                tags_list.append( el.name )
            for tag in element[2]:
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





def albums( request ):

    return render_to_response('albums.html')





def about( request ):

    return render_to_response('about.html')





def home( request ):
    
    refresh_db_with_new_data()
    #clear_db()
    try:
        last = Post.objects.order_by('-renew')[0:10]
    except Post.DoesNotExist:
        raise Http404
    
    page = 1
    pages = int(ceil(Post.objects.count() / 10.0))
    paginator = get_paginator_data( page, pages , 2 )
    num_last = len(last)
    
    return render_to_response('index.html',{ 'last':last, 'best':last, 'paginator':paginator, 'nl':num_last, 'nf':1 })

def home_page( request, page ):
    
    page = int(page)
    num_last = 10 * page
    num_first = 10 * (page - 1)
    
    try:
        last = Post.objects.order_by('-renew')[num_first:num_last]
    except Post.DoesNotExist:
        raise Http404
    
    num_first = num_first + 1
    num_last = num_first + len(last) - 1
    
    pages = int(ceil(Post.objects.count() / 10.0))
    paginator = get_paginator_data( page, pages , 2 )
    
    return render_to_response('index.html',{ 'last':last, 'paginator':paginator, 'nl':num_last, 'nf':num_first })

def photo( request, id_get ):
    
    try:
        p = Post.objects.get(id=id_get)
    except Post.DoesNotExist:
        raise Http404
    
    return render_to_response('photo.html',{ 'photo':p })

def buy( request, id_get, resolution ):
    
    try:
        p = Post.objects.get(id=id_get)
    except Post.DoesNotExist:
        raise Http404
    
    return render_to_response('buy.html',{ 'photo':p, 'res':resolution })

