from fastapi import FastAPI
from app.api.v1.routes import example, demo

app = FastAPI(title="Medium-Level FastAPI Boilerplate")

app.include_router(example.router, prefix="/api/v1/example")
app.include_router(demo.router, prefix="/api/v1/demo")


# Reload Check