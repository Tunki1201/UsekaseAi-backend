from pydantic import BaseModel, HttpUrl


class LoginPayload(BaseModel):
    client_id: str
    email: str
    first_name: str
    last_name: str
    imageUrl: str
    auth_provider: str

class ValidateUrlExists(BaseModel):
    url: HttpUrl