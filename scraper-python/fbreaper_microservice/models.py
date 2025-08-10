from typing import List, Optional
from pydantic import BaseModel

# Mirrors Java PostDTO
class PostDTO(BaseModel):
    id: str
    author: str
    content: str
    timestamp: str
    hashtags: List[str]
    language: str
    sentiment: Optional[str]

# Mirrors Java CommentDTO
class CommentDTO(BaseModel):
    id: str
    postId: str
    author: str
    text: str
    timestamp: str
    sentiment: Optional[str]

# Mirrors Java LinkAnalysisResultDTO
class LinkAnalysisResultDTO(BaseModel):
    nodes: List[dict]
    edges: List[dict]
    metrics: dict
