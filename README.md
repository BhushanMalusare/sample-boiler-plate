## Recommender system APIs

### Dependencies set-up

- Create an empty folder and clone this repository in it.

- Once cloned, next step is to create a virtual environment.

   - To create a virtual environment execute `python3 -m venv .venv`
   - To activate virtual environment, execute `source .venv/bin/activate`

- Once setting up virtual environment is done, let's install necessary packages and dependencies.

   - To do so, execute `pip install -r requirements.txt`

- This will install all the necessary packages required to run our app.

## Configuration ⚙️

- Use ReCaptcha V2
- Set environment variable
  - FA_DB_HOST
  - FA_DB_USER
  - FA_DB_PASSWORD
  - FA_DB_NAME
  - FA_JWT_KEY
  - FA_TITLE
  - FA_DESCRIPTION

## Create a symmetric key for JWT encryption 🔑

- Open terminal
- `python`
- `from jwcrypto import jwk`
- `key = jwk.JWK(generate='oct', size=256)`
- `key.export()`
- Copy value and use as `JWT_KEY`

## Create a key for fernet encryption 🔐

- Open terminal
- `python`
- `from cryptography.fernet import Fernet`
- `key = Fernet.generate_key()`
- `key.decode('utf-8')`
- Copy value and use as `FERNET_KEY`

## Running our app 🚀

- Open terminal in project root
- Run server: `uvicorn main:app --reload --host 0.0.0.0`

## Setting up token_config_template.py
- Put the generated token in global variable `TOKEN` with prefix `Bearer`

## Running unit tests on our app 🧪

- Open terminal in project root
- Execute: `python -m pytest -p no:warnings`