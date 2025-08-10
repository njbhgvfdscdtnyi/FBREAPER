import pytest
from fbreaper_microservice.schema import validate_message

def test_validate_post():
    post = {
        "id": "1",
        "author": "a",
        "content": "c",
        "timestamp": "t",
        "hashtags": [],
        "language": "en"
    }
    assert validate_message(post, 'PostDTO')

def test_invalid_schema():
    with pytest.raises(ValueError):
        validate_message({}, 'PostDTO')
    with pytest.raises(ValueError):
        validate_message({}, 'UnknownDTO')
