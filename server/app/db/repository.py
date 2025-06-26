import asyncpg
from typing import List, Dict, Optional
from app.core.config import settings
from app.core.logging import setup_logger

logger = setup_logger(__name__)


class PostRepository:
    def __init__(self):
        self.pool: Optional[asyncpg.Pool] = None

    async def connect(self):
        self.pool = await asyncpg.create_pool(
            settings.DATABASE_URL,
            min_size=1,
            max_size=10
        )
        logger.info("Database connection pool created")

    async def disconnect(self):
        if self.pool:
            await self.pool.close()
            logger.info("Database connection pool closed")

    async def init_db(self):
        if not self.pool:
            raise RuntimeError("Database pool not initialized")
        
        with open("app/db/schema.sql", "r") as f:
            schema = f.read()
        
        async with self.pool.acquire() as conn:
            await conn.execute(schema)
            logger.info("Database schema initialized")

    async def get_all_posts(self) -> List[Dict]:
        if not self.pool:
            raise RuntimeError("Database pool not initialized")
        
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(
                "SELECT id, text, created_at FROM posts ORDER BY id DESC"
            )
            return [dict(row) for row in rows]

    async def create_post(self, text: str) -> Dict:
        if not self.pool:
            raise RuntimeError("Database pool not initialized")
        
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                "INSERT INTO posts (text) VALUES ($1) RETURNING id, text, created_at",
                text
            )
            return dict(row)


post_repository = PostRepository()