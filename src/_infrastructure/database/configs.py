import os
import pathlib
import json

DATABASE_CONFIG_FILE = os.path.join(
    pathlib.Path(__file__).parent.parent.parent.parent, "storage/database_config.json")

with open(DATABASE_CONFIG_FILE) as f:
    data = json.load(f)
    POSTGRES_USER = data["user"]
    POSTGRES_PASSWORD = data["password"]
    POSTGRES_DB = data["database"]
    POSTGRES_HOST = data["host"]
