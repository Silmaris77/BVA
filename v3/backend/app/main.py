from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.dashboard import router as dashboard_router
from app.api.implants import router as implants_router

app = FastAPI(
    title="Brain Venture Academy V3 API",
    description="Neural Backend for Tactical OS",
    version="3.0.0"
)

# CORS Configuration
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Routers
app.include_router(dashboard_router)
app.include_router(implants_router)

@app.get("/")
async def root():
    return {
        "system": "BVA Tactical OS",
        "status": "ONLINE",
        "version": "v3.0.0",
        "message": "Welcome to the War Room, Operator."
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
