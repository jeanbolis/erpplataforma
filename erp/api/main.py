from fastapi import FastAPI
from erp.api.rotas import auth, financeiro, estoque, auditoria, usuarios
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="ERP API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(financeiro.router)
app.include_router(estoque.router)
app.include_router(auditoria.router)
app.include_router(usuarios.router)   # ← ESSA LINHA É OBRIGATÓRIA