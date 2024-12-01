from pydantic import BaseModel

class MessageRequest(BaseModel):
    message: str  # Define the message field as a required string