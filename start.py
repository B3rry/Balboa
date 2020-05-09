import os
from bot import Bot

# Load env and initialize bot
if os.getenv("APP_ID") is None:
    from os.path import join, dirname
    from dotenv import load_dotenv

    load_dotenv()
    # dotenv = Dotenv(os.path.join(os.path.dirname(__file__), ".env"))
    # os.environ.update(dotenv)

Bot()
