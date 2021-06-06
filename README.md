# Company User data procesor

Exercise on data transformation for company user data.

## About The Project

A typer based CLI for transforming json files based on python 3.8
It has three commands:
* `add_fullname` which extends the user to include a full_name field, using the forename and surname to generate it
* `remove_under_30s` which removes user elements based on their age, in this case any user under 30
* `resolve_company` which extends the user json with the company json, replacing the company_id attribute
### Built With

* [Typer](https://typer.tiangolo.com/)
* [Pydantic](https://pydantic-docs.helpmanual.io/)

### Installation

It is highly recommended to setup a local virtual environment for the project.

1. Install dependencies
   ```sh
   pip install -r requirements.txt
   ```
   
2. Run!
   ```sh
   python cli/transform.py --help
   ```

## Tests

This project uses pytest for running the tests. With the virtual environment activated run:
   ```sh
   pytest --cov=cli tests/
   ```