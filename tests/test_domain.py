import json
from datetime import date, timedelta

import pytest
from pydantic import ValidationError

from domain import User, UserList


def test_user_date_format():
    valid_user_dict = {
        "forename": "Git",
        "surname": "Tiago",
        "location": "United Kingdom",
        "company_id": 1
    }

    with pytest.raises(ValidationError) as e_info:
        User(**valid_user_dict, date_of_birth="1970-01-01")

    assert "time data '1970-01-01' does not match format '%Y/%m/%d'" in str(e_info.value)


def test_serialize_date_in_user_list():
    user = User(
        forename="Git",
        surname="Tiago",
        date_of_birth="1970/01/01",
        location="United Kingdom",
        company_id=1,
    )
    user_list = UserList(__root__=[user])
    user_dict_list = json.loads(user_list.json())
    assert user_dict_list[0]["date_of_birth"] == "1970/01/01"


def test_serialize_date():
    user = User(
        forename="Git",
        surname="Tiago",
        date_of_birth="1970/01/01",
        location="United Kingdom",
        company_id=1,
    )

    user_dict = json.loads(user.json())
    assert user_dict["date_of_birth"] == "1970/01/01"


def test_user_older_than():
    # Test all reasonable ages
    for age in range(0, 100):
        exact_date = date.today() - timedelta(days=365 * age)
        more_than_date = date.today() - timedelta(days=365 * age + 1)

        exactly_age_user = User(
            forename="Git",
            surname="Tiago",
            date_of_birth=exact_date,
            location="United Kingdom",
            company_id=1,
        )

        older_than_date_user = User(**{**exactly_age_user.dict(), **{"date_of_birth": more_than_date}})

        assert not exactly_age_user.is_older_than(age)
        assert older_than_date_user.is_older_than(age)


def test_full_name_creation():
    static_full_name_user = User(
        forename="Git",
        surname="Tiago",
        date_of_birth="1970/01/01",
        location="United Kingdom",
        company_id=1,
    )

    assert static_full_name_user.full_name == "Git Tiago"

    static_full_name_user = User(
        forename="Git",
        surname="Tiago",
        full_name="Git Lab Tiago",
        date_of_birth="1970/01/01",
        location="United Kingdom",
        company_id=1,
    )

    assert static_full_name_user.full_name == "Git Lab Tiago"
