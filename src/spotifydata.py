from src.auth import get_spotify_client_web
import random


def generate_data_web(access_token, game_mode, time_range, participants):
    sp = get_spotify_client_web(access_token)
    if game_mode == 'artists':
        data = sp.current_user_top_artists(limit = 50, time_range = time_range)
    elif game_mode == 'tracks':
        data = sp.current_user_top_tracks(limit = 50, time_range = time_range)
    items=data['items']
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
