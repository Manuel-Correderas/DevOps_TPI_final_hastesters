# backend/app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .db import Base, engine, init_db
from .models import models  # registra todos los modelos en Base

from .routers import (
    routes_analytics,
    routes_products,
    routes_order_items,
    routes_users,
    routes_roles,
    routes_product_comments,
    routes_orders,
    routes_comments,
    routes_auth,
    routes_cart,  
    routes_admin,
    routes_sales,
    routes_premium,
)

# === Crear app UNA sola vez ===
app = FastAPI(title="Ecom MKT Lab API")

# === CORS ===
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8501",
        "http://127.0.0.1:8501",
        # cuando tengas Render, agregás acá también la URL del frontend
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === Health check ===
@app.get("/health")
def health():
    return {"ok": True}

# === Startup ===
@app.on_event("startup")
def on_startup():
    # Crear tablas si no existen
    Base.metadata.create_all(bind=engine)
    # Inicializar datos base (roles, admin, etc.)
    init_db()

# === Routers ===
app.include_router(routes_roles.router)
app.include_router(routes_users.router)
app.include_router(routes_products.router)
app.include_router(routes_product_comments.router)
app.include_router(routes_orders.router)
app.include_router(routes_comments.router)
app.include_router(routes_auth.router)
app.include_router(routes_cart.router)
app.include_router(routes_admin.router)
app.include_router(routes_sales.router)
app.include_router(routes_order_items.router)
app.include_router(routes_analytics.router)
app.include_router(routes_premium.router)
