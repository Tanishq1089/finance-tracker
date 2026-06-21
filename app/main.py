from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from .routers import auth, expenses, budgets, reports
from .database import create_tables
import os

# Initialize database schemas
create_tables()

app = FastAPI(title="Finance Tracker", version="1.0.0")

# Enable Cross-Origin Resource Sharing (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# Include API business routers
app.include_router(auth.router)
app.include_router(expenses.router)
app.include_router(budgets.router)
app.include_router(reports.router)

# --- CLEAN SYSTEM HEALTH ENDPOINT ---
@app.get("/health")
def health_check():
    return {"status": "healthy", "message": "Session verification active"}

# --- EXPLICIT ROOT ROUTE TO SERVE FRONTEND INDEX.HTML ---
@app.get("/")
def serve_index():
    index_path = os.path.join("static", "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"error": "Frontend entry file static/index.html not found."}

# --- MOUNT STATIC ASSETS AT SUB-PATH ---
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")