
import random


def generate_data_web(sp, game_mode, time_range, participants):
    if game_mode == 'artists':
        data = sp.current_user_top_artists(limit = 50, time_range = time_range)
    elif game_mode == 'tracks':
        data = sp.current_user_top_tracks(limit = 50, time_range = time_range)
    items=data['items']
    if len(items) < participants:
        raise ValueError(f'Not enough elements. You listened to just {len(items)} {game_mode} in that time period.')
    random.shuffle(items)
    items = items[0:participants]
    participant_dictionaries=[]
    for x in range(participants):
        element = items[x]
        if game_mode == 'artists':
            participant_dictionaries.append({'name': element['name'], 'image': element['images'][0]['url']})
        elif game_mode == 'tracks':
            participant_dictionaries.append({'name': f"{element['name']} - {', '.join([artist['name'] for artist in element['artists']])}",
                                             'image': element['album']['images'][0]['url']})
        
    return participant_dictionaries

def generate_pictures(sp):
    picture_links = []
    artists_appended=[]
    for time_range in (['short_term', 'medium_term', 'long_term']):
        for artist in sp.current_user_top_artists(limit = 50, time_range = time_range)['items']:
            artist_name = artist['name']
            link = artist['images'][0]['url']
            if artist_name not in artists_appended:
                picture_links.append(link)
                artists_appended.append(artist_name)
        for track in sp.current_user_top_tracks(limit = 50, time_range = time_range)['items']:
            link = track['album']['images'][0]['url']
            if link not in picture_links:
                picture_links.append(link)
                """
                QUITADO POR DEMASIADAS CALLS A LA API
            song_artists = [artist for artist in track['artists']]
            for x in song_artists:
                artist_name = x['name']
                if artist_name not in artists_appended:
                    id = x['id']
                    song_artist = sp.artist(id)
                    link = song_artist['images'][0]['url']
                    picture_links.append(link)
                    artists_appended.append(artist_name)
                    """
    random.shuffle(picture_links)
    return picture_links

        
