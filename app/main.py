from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import app.routes.download_routes as download_routes
import app.routes.create_routes as create_routes
import app.routes.delete_routes as delete_routes
import app.routes.read_routes as read_routes
import app.routes.update_routes as update_routes

app = FastAPI()

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(create_routes.router, prefix="/create", tags=["create"])
app.include_router(read_routes.router, prefix="/read", tags=["read"])
app.include_router(update_routes.router, prefix="/update", tags=["update"])
app.include_router(delete_routes.router, prefix="/delete", tags=["delete"])
app.include_router(download_routes.router, prefix="/download", tags=["download"])