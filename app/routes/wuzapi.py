from fastapi import APIRouter
from fastapi.responses import JSONResponse
from flask import app
import httpx  # Para fazer requisições HTTP para o WUZAPI

from dotenv import load_dotenv
import os

# Carrega as variáveis do arquivo .env para o ambiente do sistema
load_dotenv()
wuzapi_url = os.getenv("WUZAPI_URL", "http://localhost:8080")  # URL do WUZAPI
wuzapi_token = os.getenv("WUZAPI_TOKEN")  # Token de autenticação do WUZAPI


router = APIRouter(prefix="/wuzapi", tags=["Wuzapi"])


@router.get("/test")
async def wuzapi_test():
    return {"success": True, "message": "Rota do Wuzapi funcionando."}


@router.post("/connect")
async def connect():
    # Dados enviados para o Wuzapi
    payload = {
        "Immediate": True
    }

    # Chama o endpoint de conexão do Wuzapi
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{wuzapi_url}/session/connect",
            headers={
                "token": wuzapi_token,
                "Content-Type": "application/json"
            },
            json=payload
        )

    print("Status Wuzapi:", response.status_code) # Adicionei um print para verificar o status da resposta do WUZAPI
    print("Resposta Wuzapi:", response.text) # Adicionei um print para verificar o conteúdo da resposta do WUZAPI

    if response.is_success:
        return response.json()

    return {
        "success": False,
        "status": response.status_code,
        "message": response.text
    }
