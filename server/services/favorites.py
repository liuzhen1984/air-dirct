import json
import os
from typing import List, Optional
from datetime import datetime
from uuid import uuid4
from models.favorite import Favorite, FavoriteCreate


class FavoritesService:
    """收藏服务 - 使用 JSON 文件存储"""

    def __init__(self, data_file: str = "data/favorites.json"):
        self.data_file = data_file
        self._ensure_data_file()

    def _ensure_data_file(self):
        """确保数据文件存在"""
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        if not os.path.exists(self.data_file):
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump({"favorites": []}, f, ensure_ascii=False, indent=2)

    def _load_favorites(self) -> List[Favorite]:
        """从文件加载收藏列表"""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return [Favorite(**item) for item in data.get("favorites", [])]
        except Exception as e:
            print(f"Error loading favorites: {e}")
            return []

    def _save_favorites(self, favorites: List[Favorite]):
        """保存收藏列表到文件"""
        try:
            data = {
                "favorites": [
                    {
                        "id": fav.id,
                        "word": fav.word,
                        "phonetic": fav.phonetic,
                        "chinese": fav.chinese,
                        "created_at": fav.created_at.isoformat(),
                    }
                    for fav in favorites
                ]
            }
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error saving favorites: {e}")
            raise

    def get_all(self) -> List[Favorite]:
        """获取所有收藏"""
        return self._load_favorites()

    def add(self, favorite_create: FavoriteCreate) -> Favorite:
        """添加收藏"""
        favorites = self._load_favorites()

        # 检查是否已收藏
        for fav in favorites:
            if fav.word.lower() == favorite_create.word.lower():
                return fav  # 已存在，返回现有记录

        # 创建新收藏
        new_favorite = Favorite(
            id=str(uuid4()),
            word=favorite_create.word,
            phonetic=favorite_create.phonetic,
            chinese=favorite_create.chinese,
            created_at=datetime.now(),
        )

        favorites.insert(0, new_favorite)  # 插入到最前面
        self._save_favorites(favorites)

        return new_favorite

    def remove(self, favorite_id: str) -> bool:
        """删除收藏"""
        favorites = self._load_favorites()
        original_count = len(favorites)

        favorites = [fav for fav in favorites if fav.id != favorite_id]

        if len(favorites) < original_count:
            self._save_favorites(favorites)
            return True
        return False

    def check(self, word: str) -> Optional[Favorite]:
        """检查单词是否已收藏"""
        favorites = self._load_favorites()
        for fav in favorites:
            if fav.word.lower() == word.lower():
                return fav
        return None
