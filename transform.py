import json
from typing import Dict, List

import typer
from typer import FileText, FileTextWrite

from domain import User, UserList

app = typer.Typer()


@app.command(name="add_fullname")
def transform_user_to_include_full_name(json_user_file: FileText, output_json_file: FileTextWrite):
    user_dicts: List[Dict] = json.load(json_user_file)
    user_list = UserList(__root__=[User(**user_dict) for user_dict in user_dicts])
    output_json_file.write(user_list.json(indent=4))


@app.command()
def transform_user_to_include_company(json_user_file: FileText, json_company_file: FileText,
                                      output_json_file: FileTextWrite):
    pass


if __name__ == "__main__":
    app()
