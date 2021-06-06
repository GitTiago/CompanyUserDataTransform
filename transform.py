import json
from typing import Dict, List

import typer
from typer import FileText, FileTextWrite

from domain import User, UserList

app = typer.Typer()


@app.command(name="add_fullname")
def add_fullname(json_user_file: FileText, output_json_file: FileTextWrite):
    user_dicts: List[Dict] = json.load(json_user_file)
    user_list = UserList(__root__=[User(**user_dict) for user_dict in user_dicts])
    output_json_file.write(user_list.json(indent=4))


@app.command(name="remove_under_30s")
def remove_under_30s(json_user_file: FileText, output_json_file: FileTextWrite):
    user_dicts: List[Dict] = json.load(json_user_file)
    user_generator = (User(**user_dict) for user_dict in user_dicts)
    user_list = UserList(__root__=[user for user in user_generator if user.is_older_than(30)])
    output_json_file.write(user_list.json(indent=4,
                                          exclude={
                                              '__root__': {
                                                  '__all__': {'full_name'}
                                              }
                                          }))


@app.command()
def transform_user_to_include_company(json_user_file: FileText, json_company_file: FileText,
                                      output_json_file: FileTextWrite):
    pass


if __name__ == "__main__":
    app()
