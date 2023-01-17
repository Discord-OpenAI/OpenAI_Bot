import os
import json

async def get_server_api_key(guild_id):
    # get the API key for the specified guild
    with open(f'server_data/{guild_id}/api_key.json', 'r') as f:
        api_key = json.load(f)
    return api_key


def set_server_api_key(guild_id, api_key):
    # create the guild's data directory if it doesn't exist
    if not os.path.exists(f'server_data/{guild_id}'):
        os.makedirs(f'server_data/{guild_id}')

    # save the API key for the specified guild
    with open(f'server_data/{guild_id}/api_key.json', 'w') as f:
        json.dump(api_key, f)
