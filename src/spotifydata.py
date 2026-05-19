from src.auth import get_spotify_client
import random

sp = get_spotify_client()

def get_user_info():
    current_user = sp.current_user()
    #print(type(sp.current_user_saved_tracks(limit=50)))
    #print(sp.current_user_saved_tracks()['items'][0]['track']['name'])
    current_user = sp.current_user()
    profile_name = current_user['display_name']
    profile_picture_link = current_user['images'][0]['url']
    print(f"Hola, {profile_name}")
    print(f"El link de tu foto de perfil, que ya lo usaré, de 300px x 300 px es {profile_picture_link}")


def generate_data(): #TAKES number RANDOM ELEMENTS FROM TOP 50, NOT NECESSARILY TOP number ELEMENTS
    time_ranges = {'1': 'short_term', '2': 'medium_term', '3': 'long_term'}
    mode = input('What do you want to play with?\n1.- Your top artists\n2.- Your top songs\nChoose 1 or 2: ')
    number = input("Select number of songs. Options are 2, 4, 8, 16 and 32: ")
    time_range = input('Select your time range:\n1.- Last month\n2.- Last 6 months\n3.- Last year\nWrite just the option number: ')
    if mode == '1':
        data = sp.current_user_top_artists(limit = 50, time_range = time_ranges[time_range])
    elif mode == '2':
        data = sp.current_user_top_tracks(limit = 50, time_range = time_ranges[time_range])

    items=data['items']
    random.shuffle(items)
    items = items[0:int(number)]
    elements_list = []
    for x in range(int(number)):
        element = items[x]
        if mode == '1':
            elements_list.append(f"{element['name']}")
        elif mode == '2':
            elements_list.append(f"{element['name']} - {', '.join([artist['name'] for artist in element['artists']])}")
        
    return elements_list