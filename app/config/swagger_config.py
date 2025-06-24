from fastapi import FastAPI

app = FastAPI(
    title="API Terê Verde",
    description="API para gerenciar atividades e eventos nos parques naturais de Teresópolis",
    version="1.0.0",
    docs_url="/api-docs",
    redoc_url="/api-redoc",
    swagger_ui_parameters={"syntaxHighlight": False}
)
