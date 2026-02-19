from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.db.session import engine, Base
import src.models.product  # register models
from src.api.products import router as product_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    Base.metadata.create_all(bind=engine)
    yield
    


app = FastAPI(
    title="High Performance Product API",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(product_router)


@app.get("/health")
def health_check():
    return {"status": "ok"}
