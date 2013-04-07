


from django.http         import Http404
from django.shortcuts    import render_to_response
from django.template     import Context, loader
from django.http         import HttpResponse
from apiclient.discovery import build
from frontend.models     import *
from sys                 import *
from django.core.mail 	 import send_mail
from django.template  	 import RequestContext
from django.http 	 import HttpResponseRedirect
from frontend.forms  	 import ReCaptchaForm







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
    request = 		  activities_resource.list(
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
			act_struct.append(activity['actor']['image']['url'] )
    		

                        act_list.append( act_struct )
			
    return act_list


def refresh_db_with_new_data( ):

    new_data = api_data_extraction()
    
    posts_list = []
    for el in Post.objects.all():
        posts_list.append( el.image_url )

    for element in new_data:
        if element[0] not in posts_list:
            p = Post( image_url = element[0] , renew = element[1] )
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

def feedback( request ):

    return render_to_response('feedback.html')



def about( request ):

    return render_to_response('about.html')





def home( request ):

    refresh_db_with_new_data()
    #clear_db()
    try:
        p = Post.objects.all()
    except Post.DoesNotExist:
        raise Http404

#    from django.core.mail import send_mail
#    send_mail('Subject here', 'Here is the message.', 'forzalino@gmail.com',
#    ['forzalino@gmail.com'], fail_silently=False)

    return render_to_response('index.html',{ 'lst':p })



def search_form(request):

    return render_to_response('search_form.html')



def contact(request):

    form = ReCaptchaForm()
    if request.POST:
        form = ReCaptchaForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            send_mail(
                cd['subject'],
                cd['message'],
                cd.get('email', 'kovalenko.stasiya@gmail.com'), ['kovalenishe@mail.ru'], fail_silently=False
           	     )

	#	send_mail('subjectsubjectsubject','me message message message message', 'lexalexa-setset@mail.ru', 'kovalenko.stasiya@gmail.com'),

            return HttpResponseRedirect('/about/')
    else:
        form = ReCaptchaForm( # initial={'subject': 'I love your site!'}
			     )
    return render_to_response('contact.html', {'form': form}, context_instance=RequestContext(request))

def thanks(request):
    return render_to_response('thanks.html')



def api_avatar_extraction():
    
    service = build(     'plus',
                         'v1', 
    developerKey =       'AIzaSyAKCO6eEQHQLN32ZARi2TOoJXVP88EZW4c')
    activities_resource = service.activities()
    request = 		  activities_resource.list(
    userId =             '100915540970866628562',                                               #'103582189468795743999',
    collection =         'public',
    maxResults =         '100' )

    
    act_photo_author = []
    activities_document = request.execute()
    if 'items' in activities_document:                                                          # if account is not empty

        for activity in activities_document['items']:                                           # taking every activity
	    act_photo_author.append(activity['actor']['image']['url'] )
    		
    return act_photo_author


