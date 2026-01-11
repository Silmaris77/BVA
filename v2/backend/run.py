"""
BVA v2 Backend Startup Script
Uruchamia FastAPI backend na porcie 8000
"""
import sys
import os

# Dodaj katalog główny do ścieżki
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

if __name__ == "__main__":
    import uvicorn
    
    # Zmień working directory na katalog główny projektu
    os.chdir(BASE_DIR)
    
    print("="*60)
    print("BrainVentureAcademy v2.0 - Backend API")
    print("="*60)
    print(f"Working directory: {os.getcwd()}")
    print(f"Base directory: {BASE_DIR}")
    print("Starting server on http://localhost:8000")
    print("API Docs: http://localhost:8000/docs")
    print("="*60)
    
    uvicorn.run(
        "v2.backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
