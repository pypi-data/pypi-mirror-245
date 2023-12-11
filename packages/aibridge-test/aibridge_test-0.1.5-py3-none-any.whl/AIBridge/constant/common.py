from AIBridge.constant.constant import FUNCTION_CALL_FORMAT, PRIORITY
from AIBridge.setconfig import SetConfig
from AIBridge.exceptions import ConfigException
from AIBridge.database.sql_service import SQL
from AIBridge.database.no_sql_service import Mongodb
from AIBridge.exceptions import AIBridgeException
from urllib.parse import urlparse
from AIBridge.output_validation.convertors import FromJson, IntoJson
import json

config = SetConfig.read_yaml()


def parse_fromat(prompt, format=None, format_structure=None):
    if format:
        prompt = prompt + f"format:json valid"
    if format_structure:
        if format:
            if format == "csv":
                format_structure = json.dumps(IntoJson.csv_to_json(format_structure))
            elif format == "xml":
                format_structure = json.dumps(IntoJson.xml_to_json(format_structure))

        prompt = prompt + f"format_structure:{format_structure}"
    prompt = (
        prompt
        + "Respond only in the exact specified format provided in the prompt,No extra information,No extra space"
    )
    return prompt


def parse_api_key(ai_service):
    if ai_service not in config:
        raise ConfigException("ai_service not found in config file")
    return config[ai_service][0]["key"]


def get_no_sql_obj():
    databse_uri = config["database_uri"]
    if "mongodb" in databse_uri:
        return Mongodb()


def get_database_obj():
    if "database" not in config:
        return SQL()
    elif config["database"] == "nosql":
        return get_no_sql_obj()
    elif config["database"] == "sql":
        return SQL()


def get_function_from_json(output_schema: dict):
    def create_function_call(output_schema: dict):
        key_dict = {"type": "object", "properties": {}}
        for key, value in output_schema.items():
            if isinstance(value, dict):
                key_dict["properties"][key] = create_function_call(value)
            elif isinstance(value, list):
                key_d = {
                    "type": "array",
                    "description": "Generate the information",
                }
                if value:
                    if isinstance(value[0], str):
                        key_d["items"] = {"type": "string", "description": value[0]}
                    elif isinstance(value[0], dict):
                        key_d["items"] = create_function_call(value[0])
                else:
                    key_d["items"] = {
                        "type": "string",
                        "description": "provide the given information",
                    }
                key_dict["properties"][key] = key_d
            else:
                key_dict["properties"][key] = {"type": "string", "description": value}
        return key_dict

    required = []
    for key in output_schema.keys():
        required.append(key)
    data = FUNCTION_CALL_FORMAT
    key_dict = create_function_call(output_schema)
    data["parameters"] = key_dict
    data["parameters"]["required"] = required
    return data


def check_url(url_list: list):
    for url in url_list:
        result = urlparse(url)
        if not all([result.scheme, result.netloc]):
            raise AIBridgeException(
                "Only image url is required, please provide valid one"
            )
    return
