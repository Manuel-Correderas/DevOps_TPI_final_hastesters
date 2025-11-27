from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db import init_db
from routes_users import router as users_router
from routes_roles import router as roles_router

from flask import Flask, request, jsonify
import sqlite3
import random

app = Flask(__name__)
DB_PATH = "palabras.db"

def conectar():
    return sqlite3.connect(DB_PATH)

app = FastAPI(title="eCom MKT Lab - Users API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501", "http://127.0.0.1:8501"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    init_db()

app.include_router(roles_router)
app.include_router(users_router)
