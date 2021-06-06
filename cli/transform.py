import json
from typing import Dict, List

import typer
from typer import FileText, FileTextWrite

from cli.domain import User, UserList, Company, CompanyUser

app = typer.Typer()


@app.command(name="add_fullname")
def add_fullname(json_user_file: FileText, output_json_file: FileTextWrite):
    """
    Adds the full_name for every user in json.
    """
    user_dicts: List[Dict] = json.load(json_user_file)
    user_list = UserList(__root__=[User(**user_dict) for user_dict in user_dicts])
    output_json_file.write(user_list.json(indent=4))


@app.command(name="remove_under_30s")
def remove_under_30s(json_user_file: FileText, output_json_file: FileTextWrite):
    """
    Removes every user currently under 30.
    """
    user_dicts: List[Dict] = json.load(json_user_file)
    user_generator = (User(**user_dict) for user_dict in user_dicts)
    user_list = UserList(__root__=[user for user in user_generator if user.is_older_than(30)])
    output_json_file.write(user_list.json(indent=4,
                                          exclude={
                                              '__root__': {
                                                  '__all__': {'full_name'}
                                              }
                                          }))


@app.command(name="resolve_company")
def resolve_company_id(json_user_file: FileText, json_company_file: FileText,
                       output_json_file: FileTextWrite):
    """
    Replaces the company_id in the user for the company with said id.
    """
    company_generator = (Company(**company_dict) for company_dict in json.load(json_company_file))
    companies_by_id = {company.id: company for company in company_generator}

    user_dicts: List[Dict] = json.load(json_user_file)
    user_generator = (User(**user_dict) for user_dict in user_dicts)
    company_user_generator = (CompanyUser(**user.dict(),
                                          company=companies_by_id[user.company_id]) for user in user_generator)
    user_list = UserList(__root__=list(company_user_generator))
    output_json_file.write(user_list.json(indent=4,
                                          exclude={
                                              '__root__': {
                                                  '__all__': {'full_name', 'company_id'}
                                              }
                                          }))


if __name__ == "__main__":
    app()
