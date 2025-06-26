from typing import List, Dict
from app.db.repository import post_repository
from app.core.logging import setup_logger

logger = setup_logger(__name__)


class PostService:
    async def get_all_posts(self) -> List[Dict]:
        posts = await post_repository.get_all_posts()
        logger.info(f"Retrieved {len(posts)} posts")
        return posts

    async def create_post(self, text: str) -> Dict:
        if not text or len(text) > 255:
            raise ValueError("Text must be between 1 and 255 characters")
        
        post = await post_repository.create_post(text)
        logger.info(f"Created post with id: {post['id']}")
        return post


post_service = PostService()