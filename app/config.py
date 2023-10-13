import dotenv
from os import environ


dotenv.load_dotenv("./env")

DATABASE_URL = environ.get("DATABASE_URL")
