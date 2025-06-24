from pymongo import MongoClient
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


def setup_database():
    try:
        client.admin.command("ping")
        print("✅ Conexão bem-sucedida com MongoDB!")
    except Exception as e:
        print("❌ Erro ao conectar ao banco:", e)
