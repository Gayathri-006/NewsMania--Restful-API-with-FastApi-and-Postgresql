from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, func, Table
from sqlalchemy.orm import relationship
from ..db.base import Base
from datetime import datetime

# Association table for many-to-many relationship between News and Category
news_categories = Table(
    "news_categories",
    Base.metadata,
    Column("news_id", Integer, ForeignKey("news.id"), primary_key=True),
    Column("category_id", Integer, ForeignKey("categories.id"), primary_key=True)
)

class News(Base):
    __tablename__ = "news"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    content = Column(Text, nullable=False)
    summary = Column(Text, nullable=True)
    image_url = Column(String, nullable=True)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    is_published = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    author = relationship("User", back_populates="news")
    categories = relationship("Category", secondary=news_categories, back_populates="news")
    favorites = relationship("Favorite", back_populates="news")

    def __repr__(self):
        return f"<News {self.title}>"
