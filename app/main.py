from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from .routers import auth, expenses, budgets, reports
from .database import create_tables 
create_tables()   # ← add this, creates all tables on startup

app = FastAPI(title="Finance Tracker", version="1.0.0")

app.add_middleware(CORSMiddleware, allow_origins=["*"],
                   allow_methods=["*"], allow_headers=["*"])

app.include_router(auth.router)
app.include_router(expenses.router)
app.include_router(budgets.router)
app.include_router(reports.router)
app.mount("/", StaticFiles(directory="static", html=True), name="static")

@app.get("/health")
def health(): return {"status": "ok"}