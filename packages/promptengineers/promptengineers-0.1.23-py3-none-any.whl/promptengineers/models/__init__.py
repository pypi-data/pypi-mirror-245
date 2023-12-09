from typing import Optional
from pydantic import BaseModel

class Retrieval(BaseModel):
    """A message to send to the chatbot."""

    provider: Optional[str] = None
    vectorstore: Optional[str] = None

    class Config:  # pylint: disable=too-few-public-methods
        """A message to send to the chatbot."""

        json_schema_extra = {
            "example": {
                "provider": "pinecone",
                "vectorstore": "Formio",
            }
        }