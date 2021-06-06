from datetime import date, datetime, timedelta
from typing import List, Any, Dict, Optional
from math import floor

from dateutil.relativedelta import relativedelta
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
        if isinstance(value, date):
            return value
        return datetime.strptime(
            value,
            DATE_FORMAT
        ).date()

    def is_underage(self):
        return not self.is_older_than(18)

    def is_older_than(self, n_years_old: int):
        n_years_ago_date = date.today() - relativedelta(years=n_years_old)
        return self.date_of_birth < n_years_ago_date

    class Config:
        json_encoders = {
            date: lambda v: v.strftime(DATE_FORMAT)
        }


class UserList(BaseModel):
    __root__: List[User]

    # Repeated config as the parent model does not necessarily use the child encoders
    # https://github.com/samuelcolvin/pydantic/issues/2277
    class Config:
        json_encoders = {
            date: lambda v: v.strftime(DATE_FORMAT)
        }


class Company(BaseModel):
    id: int
    name: str
    headquarters: str
    industry: str


class CompanyUser(User):
    company: Company
