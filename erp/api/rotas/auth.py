from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from erp.servico.usuario_servico import UsuarioServico

router = APIRouter(prefix="/auth", tags=["Autenticação"])


class LoginRequest(BaseModel):
    email: str
    senha: str


@router.post("/login")
def login(dados: LoginRequest):
    resultado = UsuarioServico.autenticar_com_token(
        email=dados.email,
        senha_plana=dados.senha
    )

    if not resultado:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    return resultado

## Se der erro apagar aqui
{
  "usuario": {...},
  "token": "JWT..."
}
