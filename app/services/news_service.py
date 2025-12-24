from typing import List, Optional, Dict, Any, Union
from datetime import datetime
from sqlalchemy import select, and_, or_, func, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from ..models.news import News, news_categories
from ..models.category import Category
from ..models.user import User
from ..schemas.news import NewsCreate, NewsUpdate
from .base import CRUDBase

class NewsService(CRUDBase[News, NewsCreate, NewsUpdate]):
    def __init__(self):
        super().__init__(News)
    
    async def get_with_categories(
        self, db: AsyncSession, id: int
    ) -> Optional[News]:
        result = await db.execute(
            select(News)
            .options(selectinload(News.categories))
            .options(selectinload(News.author))
            .filter(News.id == id)
        )
        return result.scalar_one_or_none()
    
    async def get_multi_with_author(
        self, db: AsyncSession, *, skip: int = 0, limit: int = 100
    ) -> List[News]:
        result = await db.execute(
            select(News)
            .options(selectinload(News.author))
            .order_by(desc(News.created_at))
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()
    
    async def create_with_author(
        self, db: AsyncSession, *, obj_in: NewsCreate, author_id: int, category_ids: List[int] = None
    ) -> News:
        db_obj = News(
            **obj_in.dict(exclude={"category_ids"}),
            author_id=author_id,
        )
        
        if category_ids:
            # Get the categories
            result = await db.execute(
                select(Category).filter(Category.id.in_(category_ids))
            )
            categories = result.scalars().all()
            db_obj.categories.extend(categories)
        
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj
    
    async def update_categories(
        self, db: AsyncSession, *, db_obj: News, category_ids: List[int]
    ) -> News:
        # Clear existing categories
        await db.execute(
            news_categories.delete().where(news_categories.c.news_id == db_obj.id)
        )
        
        # Add new categories
        if category_ids:
            result = await db.execute(
                select(Category).filter(Category.id.in_(category_ids))
            )
            categories = result.scalars().all()
            db_obj.categories = categories
            db.add(db_obj)
            await db.commit()
            await db.refresh(db_obj)
        
        return db_obj
    
    async def get_multi_by_author(
        self, db: AsyncSession, *, author_id: int, skip: int = 0, limit: int = 100
    ) -> List[News]:
        result = await db.execute(
            select(News)
            .filter(News.author_id == author_id)
            .order_by(desc(News.created_at))
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()
    
    async def get_multi_by_category(
        self, db: AsyncSession, *, category_id: int, skip: int = 0, limit: int = 100
    ) -> List[News]:
        result = await db.execute(
            select(News)
            .join(news_categories, News.id == news_categories.c.news_id)
            .filter(news_categories.c.category_id == category_id)
            .options(selectinload(News.author))
            .order_by(desc(News.created_at))
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()
    
    async def search(
        self, db: AsyncSession, *, search: str, skip: int = 0, limit: int = 100
    ) -> List[News]:
        search = f"%{search}%"
        result = await db.execute(
            select(News)
            .options(selectinload(News.author))
            .filter(
                or_(
                    News.title.ilike(search),
                    News.content.ilike(search)
                )
            )
            .order_by(desc(News.created_at))
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()
    
    async def get_count_by_author(self, db: AsyncSession, author_id: int) -> int:
        result = await db.execute(
            select(func.count(News.id)).filter(News.author_id == author_id)
        )
        return result.scalar() or 0

# Create a singleton instance
news = NewsService()
