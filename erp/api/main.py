from fastapi import FastAPI
from erp.api.rotas import auth, financeiro, estoque, auditoria, usuarios

app = FastAPI(title="ERP API")

app.include_router(auth.router)
app.include_router(financeiro.router)
app.include_router(estoque.router)
app.include_router(auditoria.router)
app.include_router(usuarios.router)   # ← ESSA LINHA É OBRIGATÓRIA