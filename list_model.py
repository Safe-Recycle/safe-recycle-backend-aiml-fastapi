import os

from google import genai
from google.genai import types
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from app.core.config import settings
from app.models.item_model import Item
from app.models.category_model import Category
from app.routers.item_router import BASE_STORAGE

def display_available_models() -> None:

    # Inisialisasi klien
    client = genai.Client(api_key=settings.GEMINI_API_KEY)

    # Eksekusi iterasi terhadap objek model
    try:
        model_list = client.models.list()
        for model in model_list:
            print(f"Model ID   : {model.name}")
            # Parameter atribut tambahan
            if hasattr(model, 'version'):
                 print(f"Versi      : {model.version}")
            if hasattr(model, 'description'):
                 print(f"Deskripsi  : {model.description}")
            print("-" * 60)
    except Exception as e:
         print(f"Terjadi galat komputasi atau kegagalan koneksi API: {e}")

if __name__ == "__main__":
    display_available_models()