from sqlalchemy import create_engine

from _infrastructure.database.configs import POSTGRES_DB, POSTGRES_HOST, POSTGRES_PASSWORD, POSTGRES_USER


connection_string = 'postgresql+psycopg2://{user}:{password}@{hostname}/{database}'.format(
    user=POSTGRES_USER,
    password=POSTGRES_PASSWORD,
    hostname=POSTGRES_HOST,
    database=POSTGRES_DB,
)

db_engine = create_engine(
    connection_string,
    echo=True
)
