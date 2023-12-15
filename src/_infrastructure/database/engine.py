from sqlalchemy import create_engine

from _infrastructure.database.configs import POSTGRES_DB, POSTGRES_HOST, POSTGRES_PASSWORD, POSTGRES_USER
from urllib.parse import quote_plus

connection_string = 'postgresql+psycopg2://{user}:{password}@{hostname}/{database}'.format(
    user=POSTGRES_USER,
    password=quote_plus(POSTGRES_PASSWORD),
    hostname=POSTGRES_HOST,
    database=POSTGRES_DB,
)

db_engine = create_engine(
    connection_string,
    echo=False,
    pool_size=3,
    max_overflow=7,
    pool_timeout=60,
    pool_recycle=900,
)
