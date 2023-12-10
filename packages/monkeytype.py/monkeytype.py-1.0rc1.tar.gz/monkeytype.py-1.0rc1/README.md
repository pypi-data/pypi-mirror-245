# monkeytype.py

![PyPI - Version](https://img.shields.io/pypi/v/monkeytype.py)
![Python](https://img.shields.io/badge/3.9+-Python-blue) 
![GitHub License](https://img.shields.io/github/license/m2ksims/monkeytype.py)

A wrapper built around the Monkeytype API. Find it on PyPi [here](https://pypi.org/project/monkeytype.py/).

## Installation & Usage
```
$ pip install monkeytype.py
```
### Usage
```py
import monkeytype

# You can get your API key here: https://monkeytype.com/settings#group_dangerZone
monkeytype.api_key = "YOUR_API_KEY"
user = monkeytype.User(username="maksims")

if user.is_banned:
    print(f"{user.username} is banned from monkeytype.com!")
```