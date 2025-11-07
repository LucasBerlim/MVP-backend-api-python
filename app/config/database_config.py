from pymongo import MongoClient, errors
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)
db = client["mvp"]

users_collection = db["users"]
parques_collection = db["parques"]
eventos_collection = db["eventos"]
atividades_collection = db["atividades"]

try:
    users_collection.create_index("email", unique=True)
    print("✅ Índice único em 'email' verificado/criado com sucesso.")
except errors.OperationFailure as e:
    print("⚠️ Erro ao criar índice (possivelmente já existe):", e)

def setup_database():
    try:
        client.admin.command("ping")
        print("✅ Conexão bem-sucedida com MongoDB!")
    except Exception as e:
        print("❌ Erro ao conectar ao banco:", e)
