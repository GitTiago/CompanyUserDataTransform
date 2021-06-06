import json
from tempfile import TemporaryFile
from datetime import date
from unittest.mock import patch

from cli.transform import add_fullname, remove_under_30s, resolve_company_id


def test_add_fullname():
    with TemporaryFile(mode='w+') as user_json_file, TemporaryFile(mode='w+') as output_file:
        users_json = """
        [
        {
            "forename": "Jane",
            "surname": "Smith",
            "date_of_birth": "2001/10/12",
            "location": "London",
            "company_id": 3
        },
        {
            "forename": "Mark",
            "surname": "Johnson",
            "date_of_birth": "1987/01/28",
            "location": "New York",
            "company_id": 1
        }
        ]
        """
        base_user_json_dict = json.loads(users_json)
        expected_output = [{**user_dict, **{"full_name": f"{user_dict['forename']} {user_dict['surname']}"}}
                           for user_dict in base_user_json_dict]

        user_json_file.write(users_json)
        user_json_file.seek(0)
        add_fullname(user_json_file, output_file)
        output_file.seek(0)

        added_fullname_list = json.load(output_file)
        assert expected_output == added_fullname_list


def test_remove_under_30s():
    with TemporaryFile(mode='w+') as user_json_file, TemporaryFile(mode='w+') as output_file:
        users_json = """
        [
        {
            "forename": "Jane",
            "surname": "Smith",
            "date_of_birth": "2001/10/12",
            "location": "London",
            "company_id": 3
        },
        {
            "forename": "Mark",
            "surname": "Johnson",
            "date_of_birth": "1987/01/28",
            "location": "New York",
            "company_id": 1
        }
        ]
        """
        base_user_json_list = json.loads(users_json)
        expected_output = [base_user_json_list[1]]

        user_json_file.write(users_json)
        user_json_file.seek(0)

        class NewDate(date):
            @classmethod
            def today(cls):
                return cls(year=2021, month=6, day=6)

        with patch("cli.domain.date", NewDate):
            remove_under_30s(user_json_file, output_file)
        output_file.seek(0)

        under_30s_dict = json.load(output_file)
        assert expected_output == under_30s_dict


def test_transform_user_to_include_company():
    with TemporaryFile(mode='w+') as user_json_file, TemporaryFile(mode='w+') as output_file, \
            TemporaryFile(mode='w+') as company_json_file:
        users_json = """
        [
        {
            "forename": "Jane",
            "surname": "Smith",
            "date_of_birth": "2001/10/12",
            "location": "London",
            "company_id": 3
        },
        {
            "forename": "Mark",
            "surname": "Johnson",
            "date_of_birth": "1987/01/28",
            "location": "New York",
            "company_id": 1
        }
        ]
        """
        company_json = """
        [
            {
                "id": 1,
                "name": "Company1",
                "headquarters": "City",
                "industry": "The Industry"
            },
            {
                "id": 2,
                "name": "Company2",
                "headquarters": "City",
                "industry": "The Industry"
            },
            {
                "id": 3,
                "name": "Company3",
                "headquarters": "City",
                "industry": "The Industry"
            }
        ]
        """
        base_user_json_list = json.loads(users_json)
        company_json_list = json.loads(company_json)
        expected_output_dict = [*base_user_json_list]

        del expected_output_dict[0]["company_id"]
        expected_output_dict[0]["company"] = company_json_list[2]
        del expected_output_dict[1]["company_id"]
        expected_output_dict[1]["company"] = company_json_list[0]

        user_json_file.write(users_json)
        user_json_file.seek(0)
        company_json_file.write(company_json)
        company_json_file.seek(0)

        resolve_company_id(user_json_file, company_json_file, output_file)
        output_file.seek(0)

        added_company_dict = json.load(output_file)
        assert expected_output_dict == added_company_dict
