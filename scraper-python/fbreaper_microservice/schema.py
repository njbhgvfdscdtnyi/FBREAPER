from pydantic import BaseModel, ValidationError
from .models import PostDTO, CommentDTO, LinkAnalysisResultDTO

# For strict validation of incoming/outgoing Kafka messages
SCHEMA_MAP = {
    'PostDTO': PostDTO,
    'CommentDTO': CommentDTO,
    'LinkAnalysisResultDTO': LinkAnalysisResultDTO,
}

def validate_message(data: dict, schema_name: str):
    schema = SCHEMA_MAP.get(schema_name)
    if not schema:
        raise ValueError(f"Unknown schema: {schema_name}")
    try:
        return schema(**data)
    except ValidationError as e:
        raise ValueError(f"Schema validation failed: {e}")
