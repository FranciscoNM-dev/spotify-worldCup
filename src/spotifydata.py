from src.auth import get_spotify_client_web
import random


def generate_data_web(access_token, game_mode, time_range, participants):
    sp = get_spotify_client_web(access_token)
    if game_mode == 'artists':
        data = sp.current_user_top_artists(limit = 50, time_range = time_range)
    elif game_mode == 'tracks':
        data = sp.current_user_top_tracks(limit = 50, time_range = time_range)
    items=data['items']
    if len(items) < participants:
        raise ValueError(f'Not enough elements. You listened to just {len(items)} {game_mode} in that time period.')
    random.shuffle(items)
    items = items[0:participants]
    elements_list = []
    for x in range(participants):
        element = items[x]
        if game_mode == 'artists':
            elements_list.append(f"{element['name']}")
        elif game_mode == 'tracks':
            elements_list.append(f"{element['name']} - {', '.join([artist['name'] for artist in element['artists']])}")
        
    return elements_list

def generate_pictures(access_token):
    sp = get_spotify_client_web(access_token)
    picture_links = []
    for time_range in (['short_term', 'medium_term', 'long_term']):
        for artist in sp.current_user_top_artists(limit = 50, time_range = time_range)['items']:
            link = artist['images'][0]['url']
            if link not in picture_links:
                picture_links.append(link)
        for track in sp.current_user_top_tracks(limit = 50, time_range = time_range)['items']:
            link = track['album']['images'][0]['url']
            if link not in picture_links:
                picture_links.append(link)
    random.shuffle(picture_links)
    return picture_links

        
