import os

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)  # importa as classes e funções necessárias para criar a engine e a sessão assíncrona do SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_async_engine( # cria a engine assíncrona do SQLAlchemy usando a URL do banco de dados obtida do arquivo .env
    DATABASE_URL,
    echo=True, # habilita o log de todas as instruções SQL executadas pelo SQLAlchemy, útil para depuração e monitoramento do banco de dados
)


class Base(DeclarativeBase): # define a classe base para os modelos do SQLAlchemy, que será usada como superclasse para todas as classes de modelo do banco de dados
    pass


SessionLocal = async_sessionmaker( # cria a fábrica de sessões assíncronas do SQLAlchemy, que será usada para criar sessões de banco de dados em diferentes partes do aplicativo
    bind=engine, # vincula a fábrica de sessões à engine criada anteriormente
    class_=AsyncSession, # especifica que a classe de sessão a ser usada é a AsyncSession, que permite operações assíncronas no banco de dados
    expire_on_commit=False, # especifica que os objetos carregados na sessão não devem expirar automaticamente após o commit, permitindo que eles sejam reutilizados sem precisar recarregá-los do banco de dados
)










# async def test_connection():
#     async with engine.begin() as connection: # cria um contexto assíncrono para a conexão com o banco de dados, garantindo que a conexão seja aberta e fechada corretamente
#         result = await connection.execute(text("SELECT 1")) # executa uma consulta SQL simples para testar a conexão com o banco de dados
#         print("PostgreSQL conectado:", result.scalar())