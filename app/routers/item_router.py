from uuid import uuid4
from sqlmodel import Session
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File, Form
from pathlib import Path
import math 

from app.services.item_service import read_item, create_item, show_item, update_item, delete_item
from app.schemas.item_schema import ItemListResponse, ReadItem, CreateItem, UpdateItem, SingleItemResponse
from app.databases.session import get_session

BASE_STORAGE = Path("storage/image/items")
BASE_STORAGE.mkdir(parents=True, exist_ok=True)

router = APIRouter(prefix="/items", tags=["item"])

@router.post("/", response_model=SingleItemResponse, status_code=201)
def create_item_endpoint(
    name: str = Form(...),
    description: str = Form(...),
    image: UploadFile = File(),
    recycle: str = Form(...),
    is_reusable: bool = Form(...),
    is_recyclable: bool = Form(...),
    is_hazardous: bool = Form(...),
    category_name: str = Form(...),
    session: Session = Depends(get_session)
):
    try:
        if image.content_type not in ["image/png", "image/jpg", "image/jpeg"]:
            raise HTTPException(400, "Invalid image type")
        
        filename = f"{uuid4().hex}_{image.filename}"
        filepath = BASE_STORAGE / filename
        
        with open(filepath, "wb") as f:
            f.write(image.file.read())
            
        item = create_item(
            session=session,
            data=CreateItem(
                name=name,
                description=description,
                recycle=recycle,
                image_link=str(filepath),
                is_reusable=is_reusable,
                is_recyclable=is_recyclable,
                is_hazardous=is_hazardous,
                category_name=category_name
            )
        )
        
        return {
            "status": "Success",
            "message": "Item succefully created",
            "data": item
        }
    except Exception as e:
        print(str(e))
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
        
@router.get("/{id}", response_model=SingleItemResponse)
def read_item_endpoint(id: int, session: Session = Depends(get_session)):
    item = read_item(session=session, id=id)
    
    if item is None:
        raise HTTPException(404, f"Item {id} doesn't exists")
    
    return {
        "status": "Success",
        "message": "Item succesfully retrieved",
        "data": item
    }
        
@router.get("/", response_model=ItemListResponse)
def show_items_endpoint(
    name: Optional[str] = Query(
        default=None,
        description="Search item by name"
    ),
    category: Optional[int] = Query(
        default=None,
        description="Search item by category_id"
    ),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    session: Session = Depends(get_session)
):
    offset = (page - 1) * limit
    
    items, total = show_item(
        session=session, 
        name=name, 
        category=category,
        limit=limit,
        offset=offset
    )
    
    total_pages = math.ceil(total / limit)
    
    return {
        "status": "success",
        "data": items,
        "meta": {
            "page": page,
            "limit": limit,
            "total_items": total,
            "total_pages": total_pages
        }
    }

@router.patch("/{id}", response_model=SingleItemResponse)
def update_item_endpoint(
    id: int,
    name: str | None = Form(None),
    description: str | None = Form(None),
    image: UploadFile | None = File(None),
    recycle: str | None = Form(None),
    is_reusable: bool | None = Form(None),
    is_recyclable: bool | None = Form(None),
    is_hazardous: bool | None = Form(None),
    category_name: str | None = Form(None),
    session: Session = Depends(get_session)
):
    try:
        item = read_item(session=session, id=id)
        if item is None:
            raise HTTPException(404, f"Item {id} is not found")
        
        image_path = None
        
        if image:
            if image.content_type not in ["image/jpg", "image/png", "image/jpeg"]:
                raise HTTPException(400, "Invalid image type")
            
            if item.image_link:
                old_file = Path(item.image_link)
                if old_file.exists():
                    old_file.unlink()
                    
            filename = f"{uuid4().hex}_{image.filename}"
            filepath = BASE_STORAGE / filename
            
            with open(filepath, "wb") as f:
                f.write(image.file.read())
                
            image_path = str(filepath)
        
        data_dict = UpdateItem(
            name=name,
            description=description,
            recycle=recycle,
            is_reusable=is_reusable,
            is_recyclable=is_recyclable,
            is_hazardous=is_hazardous,
            category_name=category_name
        )
        
        if image_path:
            data_dict.image_link = image_path
        
        updated = update_item(
            session=session,
            id=id,
            data=data_dict  
        )
        
        if not updated:
            raise HTTPException(404, "Item not found")
        
        return {
            "status": "Success",
            "message": "Item succefully updated",
            "data": updated
        }
        
    except Exception as e:
        raise HTTPException(400, str(e))
    
@router.delete("/{id}")
def delete_item_endpoint(
    id: int,
    session: Session = Depends(get_session)
):
    item = delete_item(session=session, id=id)
    
    if not item:
        return HTTPException(status_code=404, detail="Item not found")
    
    return {
        "status": "success",
        "message": f"Item {item.name} is deleted"
    }