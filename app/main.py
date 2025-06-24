from fastapi.middleware.cors import CORSMiddleware
from app.views.user_routes import router as user_router
from app.views.parque_routes import router as parque_router
from app.views.atividade_routes import router as atividade_router
from app.middleware.auth_middleware import setup_auth_middleware
from app.config.database_config import setup_database
from app.config.swagger_config import app

setup_database()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

setup_auth_middleware(app)

app.include_router(user_router)
app.include_router(parque_router)
app.include_router(atividade_router)


@app.get("/")
def read_root():
    return {"message": "API Terê Verde funcionando!"}
