from src.spotifydata import get_user_info, generate_data
from src.tournament import world_cup

get_user_info()


#------------------------------------------------------------------------
data = generate_data()
#------------------------------------------------------------------------
world_cup(data)
