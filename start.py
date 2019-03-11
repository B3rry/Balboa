import os
from bot import Bot

# Load env
if os.environ.get("APP_ID") is None:
    from os.path import join, dirname
    from dotenv import Dotenv

    dotenv = Dotenv(os.path.join(os.path.dirname(__file__), ".env")) # Of course, replace by your correct path
    os.environ.update(dotenv)
    # dotenv_path = join(dirname(__file__), '.env')
    # Dotenv(dotenv_path)

Bot()
