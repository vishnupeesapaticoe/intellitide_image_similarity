from pydantic import BaseModel, field_validator
from typing import List

class ImageRequest(BaseModel):
    source_url: str  # Keeping it as a string
    target_url: List[str]  # List of strings

    @field_validator("source_url")
    @classmethod
    def check_source_url(cls, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("source_url must be a non-empty string.")
        return value

    @field_validator("target_url", mode="before")
    @classmethod
    def check_target_urls(cls, value):
        if not isinstance(value, list) or not all(isinstance(item, str) and item.strip() for item in value):
            raise ValueError("target_url must be a list of non-empty strings.")
        return value