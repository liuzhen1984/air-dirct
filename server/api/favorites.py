from fastapi import APIRouter, HTTPException
from typing import List
from models.favorite import Favorite, FavoriteCreate
from services import FavoritesService

router = APIRouter(prefix="/api/favorites", tags=["favorites"])

# 初始化服务
favorites_service = FavoritesService()


@router.post("", response_model=Favorite, status_code=201)
async def add_favorite(favorite: FavoriteCreate):
    """添加收藏"""
    try:
        result = favorites_service.add(favorite)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to add favorite: {str(e)}")


@router.get("", response_model=List[Favorite])
async def get_favorites():
    """获取所有收藏"""
    try:
        favorites = favorites_service.get_all()
        return favorites
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get favorites: {str(e)}")


@router.delete("/{favorite_id}")
async def delete_favorite(favorite_id: str):
    """删除收藏"""
    success = favorites_service.remove(favorite_id)
    if not success:
        raise HTTPException(status_code=404, detail="Favorite not found")

    return {"success": True, "message": "Removed from favorites"}


@router.get("/check/{word}")
async def check_favorite(word: str):
    """检查单词是否已收藏"""
    favorite = favorites_service.check(word)

    if favorite:
        return {
            "word": word,
            "is_favorited": True,
            "favorite_id": favorite.id,
        }
    else:
        return {
            "word": word,
            "is_favorited": False,
            "favorite_id": None,
        }
