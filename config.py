import json


def get_default_config():
    default_config = {
        "region_type": "city",
        "city": "vladivostok",
        "region_number": ""
    }
    return default_config


def get_user_config():
    with open('config.json', 'r', encoding='utf-8') as js_config:
        return json.load(js_config)
