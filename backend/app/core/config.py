import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
CLERK_SECRET_KEY = os.getenv("CLERK_SECRET_KEY")