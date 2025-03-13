import os
import subprocess
from urllib.parse import urlparse
from dotenv import load_dotenv

load_dotenv()

# Configuration
LOCAL_DB_URL = os.getenv("DATABASE_URL")
HEROKU_APP = "thrive-well"
SCHEMA_FILE = "thrive-well.sql"

if not LOCAL_DB_URL:
    raise ValueError("DATABASE_URL is not set. Check your .env file.")

# Parse LOCAL_DB_URL
parsed_url = urlparse(LOCAL_DB_URL)
LOCAL_USER = parsed_url.username
LOCAL_PASSWORD = parsed_url.password
LOCAL_HOST = parsed_url.hostname
LOCAL_PORT = parsed_url.port
LOCAL_DB = parsed_url.path.lstrip("/")


def export_schema():
    """Exports the local database schema to a file."""
    cmd = [
        "pg_dump",
        "--schema-only",
        "--no-owner",
        "-h", LOCAL_HOST,
        "-U", LOCAL_USER,
        "-d", LOCAL_DB,
        "-f", SCHEMA_FILE
    ]
    env = os.environ.copy()
    env["PGPASSWORD"] = LOCAL_PASSWORD  # Avoid exposing passwords in logs

    print(f"Running: {' '.join(cmd)}")
    subprocess.run(cmd, env=env, check=True)
    print("Schema exported successfully.")


def import_schema():
    """Imports the schema file into Heroku Postgres."""
    cmd = f"heroku pg:psql -a {HEROKU_APP} < {SCHEMA_FILE}"
    print(f"Running: {cmd}")
    subprocess.run(cmd, shell=True, check=True)
    print("Schema imported successfully.")


if __name__ == "__main__":
    #export_schema()
    import_schema()
