import requests, json

api_key = "e506a1253a644591d99c117e929fc96a"
shared_secret = "98edc598aae4178ad63808fe85490b41"

def get_infos(artist, track):
    """
    Get informations according to the artist and the track
    return a dictionnary of infos if the artist and the track exists, None
    otherwise
    """
    params = {
            "include" : "minimal",
            "method" :  "track.getInfo",
            "api_key" : api_key,
            "artist" : artist,
            "track" : track,
            "format" : "json",
        }
    response = requests.get("http://ws.audioscrobbler.com/2.0", params = params, verify = False)
    track_infos = json.loads(response.text)
    if 'error' in track_infos:
        return None
    return track_infos

def get_url_image(artist, track, size):
    """
    Get the image's URL of the album where the track comes from.
    Dimensions : 64x64 pixels
    return the URL
    """
    s = size.lower()
    if s not in ['small', 'medium', 'large', 'extralarge']:
        return None
    track_infos = get_infos(artist, track)
    for image in track_infos['track']['album']['image']:
        if image['size'] == s:
            return image['#text']
    return None

def get_duration_track(artist, track):
    """
    Get the duration of the track in float
    """
    track_infos = get_infos(artist, track)
    if track_infos == None :
        return None
    return int(track_infos['track']['duration']) / 60000
