import requests


def scrape(findClass):
    list = []

    content = soup.find_all(class_=findClass)
    for element in content:
        list.append(element.string)
    
    return list

def checkDuplicate(title, artist):
    df = pd.read_csv('playlist.csv', delimiter=',')
    tuples = [tuple(x) for x in df.values]
    for t in tuples:
        if (title == t[0] and artist == t[1]):
            print("*** this song already exists in list ***")
            print("song: {}".format(t[0]))
            print("artist: {}".format(t[1]))
            return False
    
    return True

def spotifyToken(AUTH_URL, CLIENT_ID, CLIENT_SECRET):
    auth_response = requests.post(AUTH_URL, {
        'grant_type': 'client_credentials',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    })

    auth_response_data = auth_response.json()

    return auth_response_data['access_token']

def get_spotify_uri(spotifyToken, track, artist):
    query = "https://api.spotify.com/v1/search?query=track%3A{}+artist%3A{}&type=track".format(track,artist)
    
    response = requests.get(query,headers={"Content-Type": "application/json","Authorization": "Bearer {}".format(spotifyToken)})

    response = response.json()
    
    songs = response["tracks"]["items"]
    if len(songs) > 0 :
        url = songs[0]["external_urls"]["spotify"]
        return url
    else:
        return "not found"
