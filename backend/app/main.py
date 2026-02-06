from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core import database
from app import models
import os
from dotenv import load_dotenv

load_dotenv()

# Create tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="SourceTrace API V2")

# When allow_credentials is True, allow_origins cannot be ['*']
# We must explicitly list the frontend origin.
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://0.0.0.0:3000"
]

# If an env var is specifically set, add it (or overwrite)
env_origins = os.getenv("ALLOWED_ORIGINS")
if env_origins and env_origins != "*":
    origins.extend(env_origins.split(","))

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from app.api.endpoints import claims
app.include_router(claims.router, prefix="/api/claims", tags=["claims"])

@app.get("/")
def read_root():
    return {"message": "SourceTrace V2 API Running"}
