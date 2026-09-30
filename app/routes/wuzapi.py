from fastapi import APIRouter, HTTPException  # noqa: I001
import httpx  # Para fazer requisições HTTP para o WUZAPI

from dotenv import load_dotenv
import os

# Carrega as variáveis do arquivo .env para o ambiente do sistema
load_dotenv()
wuzapi_url = os.getenv("WUZAPI_URL", "http://localhost:8088")  # URL do WUZAPI
token_admin = str(os.getenv("WUZAPI_ADMIN_TOKEN"))  # Token de autenticação do WUZAPI
token_user = str(os.getenv("WUZAPI_USER_TOKEN"))  # Token de autenticação do WUZAPI
#print("Wuzapi-token", token_admin)
#print("Wuzapi-token", token_user)

router = APIRouter(prefix="/wuzapi", tags=["Wuzapi"])


@router.get("/test")
async def wuzapi_test():
    return {"success": True, "message": "Rota do Wuzapi funcionando."}


# Cria um usuário no Wuzapi, que será usado para conectar a sessão do WhatsApp
@router.post("/user/create")
async def create_user():
     # O token admin autoriza a criação; o token abaixo será a credencial
    # do usuário para conectar uma sessão do WhatsApp.
    if not token_admin or not token_user:
        raise HTTPException(
            status_code=500,
            detail="Configure WUZAPI_ADMIN_TOKEN e WUZAPI_USER_TOKEN no .env.",
        )

    # A documentação mostra name e token como campos de criação.
    # Não inclua webhook/events até confirmar o schema dessa versão do Wuzapi.
    payload = {
        "name": "agente-entrega",
        "token": token_user,
        
    }

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.post(
                f"{wuzapi_url}/admin/users",
                # A API documenta o token admin no header Authorization.
                headers={"Authorization": token_admin},
                json=payload,
            )
    except httpx.RequestError:
        raise HTTPException(
            status_code=502,
            detail="Não foi possível comunicar com o Wuzapi.",
        )

    if not response.is_success:
        # Não devolva detalhes internos do serviço diretamente ao navegador.
        raise HTTPException(
            status_code=response.status_code,
            detail="O Wuzapi não conseguiu criar o usuário.",
        )

    return {"success": True, "message": "Usuário criado no Wuzapi."}





# conecta após criar o usuário, para iniciar a sessão do WhatsApp
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
                "token": token_user,
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



@router.get("/qrcode")
async def get_qrcode():
        # Chama o endpoint de QR code do Wuzapi
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{wuzapi_url}/session/qr",
                headers={
                    "token": token_user,
                    "Content-Type": "application/json"
                }
            )

        if response.is_success:
            return response.json()

        return {
            "success": False,
            "status": response.status_code,
            "message": response.text
        }




@router.post("/disconnect")
async def disconnect():
    # Chama o endpoint de desconexão do Wuzapi
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{wuzapi_url}/session/disconnect",
            headers={
                "token": token_user,
                "Content-Type": "application/json"
            }
        )

    if response.is_success:
        return response.json()

    return {
        "success": False,
        "status": response.status_code,
        "message": response.text
    }

@router.get("/status")
async def get_status():
    # Chama o endpoint de status do Wuzapi
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{wuzapi_url}/session/status",
            headers={
                "token": token_user,
                "Content-Type": "application/json"
            }
        )

    if response.is_success:
        return response.json()

    return {
        "success": False,
        "status": response.status_code,
        "message": response.text
    }


@router.get("/group")
async def get_groups():
    # Chama o endpoint de grupos do Wuzapi
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{wuzapi_url}/group/list",
            headers={
                "token": token_user,
                "Content-Type": "application/json"
            }
        )

    if response.is_success:
        return response.json()

    return {
        "success": False,
        "status": response.status_code,
        "message": response.text
    }