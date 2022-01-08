from fastapi import FastAPI, APIRouter
import uvicorn
from starlette.middleware.cors import CORSMiddleware
from models.database import database
from routers import customers
from core.config import settings



app = FastAPI(title="BankMin API", openapi_url="/openapi.json")
api_router = APIRouter()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(customers.router)

if __name__ == '__main__':
    uvicorn.run(app, port=8000, host='0.0.0.0')
