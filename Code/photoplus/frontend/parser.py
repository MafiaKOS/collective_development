import sys
from apiclient.discovery import build

service = build(
       'plus', 
       'v1', 
       developerKey='AIzaSyAKCO6eEQHQLN32ZARi2TOoJXVP88EZW4c')
activities_resource = service.activities()
request = activities_resource.list(
       userId= '100915540970866628562',#'103582189468795743999',
       collection='public',
       maxResults='10' )


def get_tags_list(hashstring):
  spis = []
  for e in range( 0,hashstring.count("ot-hashtag") ):
    r = hashstring.find('#')+1
    hashstring = hashstring[r:]
    t = hashstring.find('<')
    spis.append( hashstring[:t] )
  print spis


activities_document = request.execute()
var = []
if 'items' in activities_document:
  for activity in activities_document['items']:
    if 'actor' not in activity['object']:
      if 'attachments' in activity['object']:
        print activity['object']['attachments'],"\n\n"#[0]['fullImage']['url']
#      hash_tag_string = activity['object']['content']
#      get_tags_list( hash_tag_string )