import os

from dotenv import load_dotenv

load_dotenv()

PROD = os.getenv("PROD")
SCHEMA = os.getenv("PG_SCHEMA", "")
HOST = os.getenv("PG_HOST", "")
PORT = os.getenv("PG_PORT", "")
USER = os.getenv("PG_USER", "")
PASSWORD = os.getenv("PG_PASSWORD", "")
PG_URL = os.getenv("PG_URL", None)
DEBUG = PROD is None

ALLOW_TOKEN = ["hMRSNSNiw3tAh33cLwCGhXeZDs4zNyeMnGwhoFjH6vavT"]
