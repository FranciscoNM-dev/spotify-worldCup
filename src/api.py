from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from src.auth import get_token_code, get_auth_url, get_spotify_client_web, refresh_access_token
from src.spotifydata import generate_data_web, generate_pictures
import json
from fastapi.staticfiles import StaticFiles
from spotipy.exceptions import SpotifyException #Para manejar errores de token


app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def home_page(request: Request):
    return templates.TemplateResponse(
        request=request, name="index.html"
    )

@app.get("/login", response_class=RedirectResponse)
async def logging_in():
    return RedirectResponse(get_auth_url())

@app.get("/callback")
async def callback(code: str):
    token_info = get_token_code(code)
    response = RedirectResponse("/game")
    response.set_cookie(key="access_token", value=token_info['access_token']) #access token
    response.set_cookie(key="refresh_token", value=token_info['refresh_token']) #refresh token
    return response

@app.get("/game", response_class=HTMLResponse)
async def game_page(request: Request):

    access_token = request.cookies['access_token']
    refresh_token = request.cookies['refresh_token']
    try: #Si todo va bien (el token no ha caducado)
        spClient = get_spotify_client_web(access_token)
        username = spClient.current_user()['display_name']
        
    except SpotifyException as e: #Si hay excepción de Spoti
        if e.http_status == 401: #Y esa excepción es por token caducado
            access_token = refresh_access_token(refresh_token)  # pide token nuevo
            sp = get_spotify_client_web(access_token)           # crea cliente nuevo
            username = sp.current_user()['display_name']        # reintenta

    error = request.cookies.get('error', None)
    response = templates.TemplateResponse(
        request=request, name="game.html", context={"username": username, "error": error}
    )
    response.set_cookie(key="access_token", value=access_token)  # actualiza token si renové
    if error:
        response.delete_cookie("error")

    return response

@app.post("/game_start", response_class=RedirectResponse) #ESTE ES .post, NO .get
#Es post porque recoge lo del formulario que le enviamos desde /game a partir de game.html
async def game_start(request: Request, game_mode: str = Form(...), time_range: str = Form(...), participants: int = Form(...)): 
    #Lo que importa es el nombre del param. Va a Form a buscar ese nombre en particular
    access_token = request.cookies['access_token']
    refresh_token = request.cookies['refresh_token']
    sp = get_spotify_client_web(access_token)
    try:
        participant_dictionaries = generate_data_web(sp, game_mode, time_range, participants)
    except ValueError as e:
        response = RedirectResponse("/game", status_code=303)
        response.set_cookie(key='error', value = str(e))
        return response
    except SpotifyException as e:
        if e.http_status == 401:
            access_token = refresh_access_token(refresh_token)  # pide token nuevo
            sp = get_spotify_client_web(access_token)
            try:
                participant_dictionaries = generate_data_web(sp, game_mode, time_range, participants)
            except ValueError as e:
                response = RedirectResponse("/game", status_code=303)
                response.set_cookie(key='error', value = str(e))
                return response
    bracket = [[participant_dictionaries[x], participant_dictionaries[x+1]] for x in range(0,len(participant_dictionaries),2)]
    response = RedirectResponse("/battle", status_code=303)
    response.set_cookie(key="bracket", value=json.dumps(bracket))
    response.set_cookie(key='index', value=0)
    response.set_cookie(key='round', value=1)
    response.set_cookie(key='round_winners', value = json.dumps([]))
    response.set_cookie(key='access_token', value = access_token)
    return response

@app.get("/battle", response_class=HTMLResponse)
async def game_round(request: Request):
    index = int(request.cookies['index'])
    bracket = json.loads(request.cookies['bracket'])
    round = int(request.cookies['round'])
    round_matches = len(bracket)
    contender_1=bracket[index][0]
    contender_2=bracket[index][1]
    return templates.TemplateResponse(request = request, name = 'battle.html',
                                      context={'battle': index+1, 'round_matches': round_matches,'round': round,
                                      'contender_1': contender_1, 'contender_2': contender_2})
        

@app.post("/battle", response_class=RedirectResponse)
async def proccess_choice(request: Request, winner = Form(...)):
    print(winner)
    response = RedirectResponse("/battle", status_code=303)
    index = int(request.cookies['index'])
    round_winners = json.loads(request.cookies['round_winners'])
    print(round_winners)
    bracket = json.loads(request.cookies['bracket'])
    round = int(request.cookies['round'])
    round_winners.append(winner)
    if len(round_winners)==len(bracket):
        round_winners = [json.loads(round_winner) for round_winner in round_winners]
        if len(round_winners) == 1: #Hay ganador
            response = RedirectResponse("/winner", status_code = 303)
            response.set_cookie(key = 'winner', value = json.dumps(round_winners[0]))
            return response
        bracket = [[round_winners[x], round_winners[x+1]] for x in range(0,len(round_winners),2)]
        round_winners = []
        response.set_cookie(key = 'round', value = round + 1)
        response.set_cookie(key = 'bracket', value = json.dumps(bracket))
        index = -1
    response.set_cookie(key = 'index', value = index+1)
    response.set_cookie(key='round_winners', value = json.dumps(round_winners))
    return response

@app.get("/winner", response_class=HTMLResponse)
async def winner(request: Request):
    winner = json.loads(request.cookies['winner'])
    return templates.TemplateResponse(
        request=request, name="winner.html", context={"winner": winner}
    )

@app.get("/logout", response_class=RedirectResponse)
async def logout(request: Request):
    response = RedirectResponse("/")
    for cookie in request.cookies.keys():
        response.delete_cookie(cookie)
    return response

@app.get("/images") #Este "endpoint" es bastante importante para el script de /game
async def get_images(request: Request):
    access_token = request.cookies['access_token']
    sp = get_spotify_client_web(access_token)
    return generate_pictures(sp)
    

