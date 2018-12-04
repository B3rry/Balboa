import os
from bot import Bot

# Load env
if os.environ.get("APP_ID") is None:
    from os.path import join, dirname
    from dotenv import load_dotenv

    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)

Bot()
