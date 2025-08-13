from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.engine import URL

url_object = URL.create(
    "postgresql+asyncpg",
    username="venkatesan",
    password="Sriviviji@101",
    host="localhost",
    port="5432",
    database="newsstand"
    )

Base = declarative_base()

async_engine = create_async_engine(url_object, echo=True)

async_session = sessionmaker(bind=async_engine, class_=AsyncSession, expire_on_commit=False)

async def get_async_session() ->AsyncSession:
    async with async_session() as session:
        yield session
