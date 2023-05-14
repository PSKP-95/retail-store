from time import time
from fastapi import Request
from app.config import settings
from app.database import create_db_connection
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from auth.route import router as ItemRouter
from fastapi.middleware.gzip import GZipMiddleware

import uvicorn



def get_application():
    _app = FastAPI(title=settings.PROJECT_NAME)

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    _app.add_middleware(GZipMiddleware, minimum_size=10)

    return _app


app = get_application()

create_db_connection()


# add all routers
app.include_router(ItemRouter, prefix="/iam", tags=["iam"])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
