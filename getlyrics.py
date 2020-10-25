# for testing API

from urllib.request import urlopen, Request

def getLyrics(artist, title):
    request = Request("https://api.lyrics.ovh/v1/"+artist+"/"+title)
    response_body = urlopen(request).read()
    print(response_body)
    
getLyrics("eminem", "rap_god")