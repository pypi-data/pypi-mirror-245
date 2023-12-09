from datetime import datetime

from pydantic import BaseModel, StrictStr, StrictBool, Field, StrictInt
from typing import Union, Optional, Literal, List, Any
from functools import wraps

class APIBaseResponse(BaseModel):
    status: Optional[Literal["success", "error"]] = "error"
    message: Optional[StrictStr] = None
    error_messages: Optional[Union[List[Any], Any]] = None
    validation_errors: Optional[Any] = Field(alias="detail", default=None)

class IEmailRecipient(BaseModel):
    email: StrictStr
    pre_header_name: StrictStr


class IEmailIntegrationData(BaseModel):
    active: StrictBool
    recipients: Union[List[IEmailRecipient], None] = None


class UpdateEmailRecipientsPayload(BaseModel):
    action: Literal["overwrite", "add", "remove"]
    emails: List[IEmailRecipient]


class WhatsappRecipient(BaseModel):
    country_code: StrictStr
    country_dial_code: StrictInt
    country_name: StrictStr
    phone_number: StrictInt


def input_model(func):
    @wraps(func)
    def wrapper(self, **kwargs):
        model_fields = func.__annotations__
        validated_payload = {}

        for field_name, field_type in model_fields.items():
            if field_name in kwargs:
                validated_payload[field_name] = field_type(kwargs[field_name])

        return func(self, validated_payload)

    return wrapper


class Client(BaseModel):
    id: StrictStr
    name: StrictStr
    created_at: datetime
    updated_at: datetime


class UserType(BaseModel):
    id: Literal["client-owner", "workspace-member", "process-member", "worker"]
    name: StrictStr