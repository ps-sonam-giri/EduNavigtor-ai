"""Auth schemas."""

from typing import Any

from pydantic import BaseModel, field_serializer


class UserResponse(BaseModel):
    id: Any
    email: str
    full_name: str
    is_active: bool
    is_verified: bool

    @field_serializer('id')
    def serialize_uuid(self, v: Any) -> str:
        return str(v)

    model_config = {"from_attributes": True}
