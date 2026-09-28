from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.routes.wuzapi import router as wuzapi_router # Importa o roteador do Wuzapi

# Cria a aplicação FastAPI
app = FastAPI(
    title="Agente ZAP",
    version="1.0"
)

# Arquivos estáticos: CSS, JavaScript, imagens etc.
app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static"
)
# Arquivos JavaScript
app.mount(
    "/script",
    StaticFiles(directory="app/script"),
    name="script"
)


# Define a pasta onde estão nossos arquivos HTML
templates = Jinja2Templates(directory="app/templates")

# Registra o roteador do Wuzapi na aplicação FastAPI
app.include_router(wuzapi_router)



# Rota principal
@app.get("/")
async def home(request: Request): # Recebe o objeto de requisição como parâmetro
    # Renderiza o index.html
    return templates.TemplateResponse(
       request=request, # Passa o objeto de requisição para o template
        name="index.html" # Nome do arquivo HTML a ser renderizado
        
    )


