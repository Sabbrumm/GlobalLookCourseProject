from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import NullPool
from config import config

"""
Используем асинхронную библиотеку для работы с базой данных postgresql
Для генератора надо использовать синхронную!

pip install asyncpg
pip install psycopg2

- sabbrumm
"""


CREDENTIALS = f'{config.database.database_login()}:{config.database.database_password()}' \
              f'@' \
              f'{config.database.database_ip()}:{config.database.database_port()}'
DATABASE_URL = f'postgresql+asyncpg://{CREDENTIALS}/{config.database.database_name()}'

Base = declarative_base()


async_engine = create_async_engine(DATABASE_URL, poolclass=NullPool)
async_session_factory: sessionmaker = sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

