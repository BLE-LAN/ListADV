## ListADV

A simple web to store and list in tables the BLE ADV given in JSON by the API. Programmed with Flask (Python 3) and SQlite.

## Dependencies

The requirements.txt file is added in the root path, the main packages are:

* Flask -> the framework
* flask-expects-json -> used to valide the requets body in JSON
* Flask-JWT-Extended -> generate and control some url access with JWT

### Build


Clone the repository

```
  git clone https://github.com/BLE-LAN/ListADV
```

Create a Virtual Environment.

```
  python3 -m venv listdadv-env
  source listdadv-env/bin/activate
```

Install the requirements.txt or add manually the packages liste in [Dependencies](##Dependencies) section.

```
  python -m pip install -r ListADV/requirements.txt
```

## Some screenshots
