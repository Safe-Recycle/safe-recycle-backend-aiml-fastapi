import gdown
import os

from app.core.config import settings
from app.databases.session import get_session
from app.services.category_service import create_category
from app.schemas.category_schema import CreateCategory

folder_path = "storage/image/categories"
session = next(get_session())

# Download files from google drive
gdown.download_folder(
    settings.GOOGLE_DRIVE_CATEGORIES, 
    output=folder_path,
    quiet=False
)

# Remove files
remove_files = [
    'other.png',
    'no-internet.png',
    'no-results.png',
    'non-recycleable.png',
    'recycleable.png',
    'non-reusable.png',
    'other.png',
    'reusable.png',
    'x.png'
]

for filename in remove_files:
    filepath = os.path.join(folder_path, filename)
    
    if os.path.exists(filepath):
        os.remove(filepath)
        print(f"{filename} is removed")
    else:
        print(f"{filename} tidak ditemukan")

# Seed data to database
for file in os.listdir(folder_path):
    try:
        filepath = os.path.join(folder_path, file)
        if not os.path.isfile(filepath):
            continue
        filename = os.path.splitext(file)[0]
        
        category = create_category(
            session=session,
            data=CreateCategory(
                name=filename,
                image_link=str(filepath)
            )
        )
        
        print(f"{filename} seeded")
    except Exception as e:
        print(f"{file} failed to seed: {e}")

print("Seeder is fully completed")