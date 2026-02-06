from uuid import uuid4
from sqlmodel import Session
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File, Form
from pathlib import Path

from app.services.category_service import read_category, show_category, create_category, update_category, delete_cetegory
from app.databases.session import get_session
from app.schemas.category_schema import ReadCategory, CreateCategory

BASE_STORAGE = Path("storage/image/categories")
BASE_STORAGE.mkdir(parents=True, exist_ok=True)

router = APIRouter(prefix="/categories", tags=["category"])

@router.get("/{id}")
def read_category_endpoint(id: int, session: Session = Depends(get_session)):
    category = read_category(session, id)
    
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    return category

@router.get("/", response_model = List[ReadCategory])
def show_categories_endpoint(
    name: Optional[str] = Query(
        default=None,
        description="Search category by name"
    ),
    session: Session = Depends(get_session)
):
    return show_category(session=session, name=name)

@router.post("/", response_model=ReadCategory, status_code=201)
def create_category_endpoint(
    name: str = Form(...),
    image: UploadFile = File(), 
    session: Session = Depends(get_session)
):
    try:
        if image.content_type not in ["image/png", "image/jpg"]:
            raise HTTPException(400, "Invalid image type")
        
        filename = f"{uuid4().hex}_{image.filename}"
        filepath = BASE_STORAGE / filename
        
        # print(filepath)
        
        with open(filepath, "wb")  as f:
            f.write(image.file.read())
        
        category = create_category(
            session=session,
            data=CreateCategory(
                name=name,
                image_link=str(filepath)
            )
        )

        return category
            
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
        
@router.put("/{id}", response_model=ReadCategory)
def update_category_endpoint(
    id: int,
    name: str | None = Form(None),
    image: UploadFile | None = File(None),
    session: Session = Depends(get_session)
):
    try:
        category = read_category(session=session, id=id)
        if not category:
            raise HTTPException(404, "Category not found")
        
        image_path = None
        
        if image:
            if image.content_type not in ["image/png", "image/jpeg", "image/jpg"]:
                raise HTTPException(400, "Invalid image type")
            
            if category.image_link:
                old_file = Path(category.image_link)
                if old_file.exists():
                    old_file.unlink()
            
            filename = f"{uuid4().hex}_{image.filename}"
            filepath = BASE_STORAGE / filename
            
            with open(filepath, "wb") as f:
                f.write(image.file.read())

            image_path = str(filepath)
            
        updated = update_category(
            session=session,
            id=id,
            name=name,
            image_link=image_path
        )
        
        if not updated:
            raise HTTPException(404, "Category not found")
        
        return updated
    except Exception as e:
        raise HTTPException(400, str(e))
    
@router.delete("/{id}")
def delete_category_endpoint(
    id: int,
    session: Session = Depends(get_session)
):
    category = delete_cetegory(session=session, id=id)
    
    if not category:
        return HTTPException(status_code=404, detail="Category not found")
    
    return {
        "status": "success",
        "message": "Category is deleted"
    }