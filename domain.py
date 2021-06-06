from datetime import date, datetime
from typing import List, Any, Dict, Optional

from pydantic import BaseModel, validator

DATE_FORMAT = "%Y/%m/%d"


class User(BaseModel):
    forename: str
    surname: str
    full_name: Optional[str]
    date_of_birth: date
    location: str
    company_id: int

    @validator("full_name", pre=True, always=True)
    def full_name_validator(cls, value: Optional[str], values: Dict[str, Any]):
        if isinstance(value, str):
            return value
        else:
            return f"{values.get('forename')} {values.get('surname')}"

    @validator("date_of_birth", pre=True)
    def parse_birthdate(cls, value):
        return datetime.strptime(
            value,
            DATE_FORMAT
        ).date()

    class Config:
        json_encoders = {
            date: lambda x: x.strftime(DATE_FORMAT)
        }


class UserList(BaseModel):
    __root__: List[User]


class Company(BaseModel):
    id: int
    name: str
    headquarters: str
    industry: str
