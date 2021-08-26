## ListADV

A simple web to store and list the BLE ADV given in JSON by the API. Programmed with Flask (Python 3) and SQlite.

## Dependencies

The requirements.txt file is added in the root path, the main packages are:

* Flask -> the framework
* flask-expects-json -> used to validate the request JSON body.
* Flask-JWT-Extended -> generate and control some url access with JWT

## Build

Clone the repository

```
  git clone https://github.com/BLE-LAN/ListADV
```

Create a Virtual Environment.

```
  python3 -m venv listdadv-env
  source listdadv-env/bin/activate
```

Install the requirements.txt or add manually the packages listed in [Dependencies](##Dependencies) section.

```
  python -m pip install -r ListADV/requirements.txt
```

In the root repo folder setup some env variables and init de database. In production FLASK_ENV must not be set. The command 'init-db' is a custom command for delete all the tables and create the sqlite file if it is needed.

```
  export FLAS_APP=listadv
  export FLASK_ENV=development
  flask init-db
  flask run
```

## API

The steps to send a list of devices with the API are (I use the HTTPie tool but curl or another is ok):

1. Login with a POST request in the /api/login URL.

```
$ https POST https://nyaboron.pythonanywhere.com/api/login username="$USER" password="$PASS"

HTTP/1.0 200 OK
Content-Length: 289
Content-Type: application/json

{ "access_token": "YOUR_JWT" }
```

2. Send a POST request with the auth header.

```
$ https --auth-type=jwt --auth="YOUR_JWT" POST https://nyaboron.pythonanywhere.com/api/adddevices < input_adv.json

HTTP/1.0 200 OK
Content-Length: 34
Content-Type: application/json

{ "added": 2, "updated": 0}
```

## List ADV JSON schema

The JSON object scheme is validated, if some field is not correct the request will we reject why the backend.
This is a example of a valid body.

```
{
  "devices": [
    {"address":"7C:A1:5D:94:1E:53","advtype":"ConnectableUndirected","rssi":-95,"timestamp":"Thu Aug 12 11:05:14 2021","unknowns":[{"type":"FF","raw":"89 00 50 02 94 00 54 58"},{"type":"2","raw":"FE FE"},{"type":"1","raw":"04"}]}
  ]
}
```

Is a json array called "devices", each array item is a object. Fields address, advtype, rssi and timestamp must be in the object. The field "unkowns" is optional.

## Some screenshots

Fixed navbar with login/register button.

![index1](https://github.com/BLE-LAN/ListADV/blob/main/readme_resources/index.jpg)

Login and register validation.

![register](https://github.com/BLE-LAN/ListADV/blob/main/readme_resources/register_fail.jpg)

After logi, user can see the list of devices. It is a bootstrap table with ajax pagination.

![register](https://github.com/BLE-LAN/ListADV/blob/main/readme_resources/table.jpg)

After pressing the 'show' another box is opened below the table with the data types. In that example any data is known that's why the raw bytes are given.

![register](https://github.com/BLE-LAN/ListADV/blob/main/readme_resources/detail.jpg)

Users can go to the devices table with a button in the index.

![register](https://github.com/BLE-LAN/ListADV/blob/main/readme_resources/index_after_login.jpg)
