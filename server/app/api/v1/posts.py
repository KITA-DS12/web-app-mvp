from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import List
from app.api.deps import get_post_service_dep
from app.services.post_service import PostService

router = APIRouter()


class PostCreate(BaseModel):
    text: str = Field(..., min_length=1, max_length=255)


class PostResponse(BaseModel):
    id: int
    text: str


@router.get("/posts", response_model=List[PostResponse])
async def get_posts(
    post_service: PostService = Depends(get_post_service_dep)
):
    posts = await post_service.get_all_posts()
    return posts


@router.post("/posts", response_model=PostResponse)
async def create_post(
    post_data: PostCreate,
    post_service: PostService = Depends(get_post_service_dep)
):
    try:
        post = await post_service.create_post(post_data.text)
        return post
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))