import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import URL, create_engine

project_root = Path(__file__).resolve().parents[2]
load_dotenv(project_root / ".env", override=False)

database_url = URL.create(
    drivername="postgresql+psycopg",
    username=os.getenv("POSTGRES_USER", "taskops"),
    password=os.environ["POSTGRES_PASSWORD"],
    host=os.getenv("POSTGRES_HOST", "127.0.0.1"),
    port=int(os.getenv("POSTGRES_PORT", "5433")),
    database=os.getenv("POSTGRES_DB", "taskops"),
)

engine = create_engine(
    database_url,
    pool_pre_ping=True,
    connect_args={"connect_timeout": 3},
)
