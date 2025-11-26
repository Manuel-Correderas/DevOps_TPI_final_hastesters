import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Leemos la URL desde las variables de entorno
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    # Mensaje claro por si te olvidás de setearla
    raise RuntimeError(
        "DATABASE_URL no está definida. "
        "Configuralá en tu .env (local) o en las variables de entorno de Render."
    )

# Creamos el engine de SQLAlchemy
engine = create_engine(DATABASE_URL, echo=False)

# Sesión por request
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# Base para los modelos
Base = declarative_base()
