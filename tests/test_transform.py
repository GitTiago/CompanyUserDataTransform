import json
import tempfile

from transform import add_fullname


def test_add_fullname():
    with tempfile.TemporaryFile(mode='w+') as user_json_file, tempfile.TemporaryFile(mode='w+') as output_file:
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
        expected_output_dict = [{**user_dict, **{"full_name": f"{user_dict['forename']} {user_dict['surname']}"}}
                                for user_dict in base_user_json_dict]

        user_json_file.write(users_json)
        user_json_file.seek(0)
        add_fullname(user_json_file, output_file)
        output_file.seek(0)

        added_fullname_dict = json.load(output_file)
        assert expected_output_dict == added_fullname_dict
