# monkeytype.py

![Python](https://img.shields.io/badge/3.10+-Python-blue) 
![GitHub License](https://img.shields.io/github/license/m2ksims/monkeytype.py)

A wrapper built around the Monkeytype API.

## Installation & Usage

```
$ pip install monkeytype.py
```
### Usage

```py
import requests
import monkeytype

# You can get your API key here: https://monkeytype.com/settings#group_dangerZone
client = monkeytype.Client(api_key="API_KEY_HERE")
user = monkeytype.User(
    client=client,
    username="maksims"
)

if user.is_banned:
    print(f"{user.username} is banned from monkeytype.com!")
```