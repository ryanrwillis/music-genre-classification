# pip install ksoftapi first
# 
import ksoftapi

kclient = ksoftapi.Client('6MdqqkQ8sSC0WB4i8PyRuQ')

async def find_lyrics(query: str):
    try:
        results = await kclient.music.lyrics(query)
    except ksoftapi.NoResults:
        print('No lyrics found for ' + query)
    else:
        first = results[0]
        print(first.lyrics)

find_lyrics("No Diggity")