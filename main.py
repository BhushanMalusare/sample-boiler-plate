from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import config
from routers.v1 import api as v1

app = FastAPI(
    title=config.TITLE,
    description=config.DESCRIPTION,
    version="1.0.0",
    redoc_url=None,
)
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(v1.router)
