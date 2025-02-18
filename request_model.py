from pydantic import BaseModel

class ImageRequest(BaseModel):
    source_url : str
    target_url : list
