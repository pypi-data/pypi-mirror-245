from datetime import datetime
import yaml
import re

def get_nested_dict(nested_dict, keys, parameters, level):
    if type(nested_dict) is dict:
        if(keys[0] in nested_dict.keys()):
            return get_nested_dict(nested_dict[keys[0]], keys[1:], parameters, level)
        else:
            return None
    elif type(nested_dict) is list:
        if len(keys) == 0:
            return "__is_list__"

        level_parameters = next((x for x in parameters if x["name"] == level), "default")
        level_parameters["name"] = keys[0]

        for list_item in nested_dict:
            check_conf_file(list_item, [level_parameters])

        return "__is_list__"
    else:
        return nested_dict

def set_nested_dict(nested_dict, keys, new_value):
    if(new_value == "__is_list__"):
        return

    if len(keys) == 1:
        nested_dict[keys[0]] = new_value
    else:
        key = keys[0]
        if key in nested_dict:
            set_nested_dict(nested_dict[key], keys[1:], new_value)

def convert_timestamp_format(timestamp):
    if timestamp == "":
        return "%Y%m%d"

    timestamp = timestamp.replace("yyyy", "%Y")
    timestamp = timestamp.replace("mm", "%m")
    timestamp = timestamp.replace("dd", "%d")
    return timestamp

def set_variable_value(value, variables):
    if type(value) is dict or type(value) is list or value == None:
        return value

    for match in re.findall(r"((var|sys)\.([\w\d]+)(\('([\w\d\/\\ \-]+)'\)){0,1})", value):
        old_value, mode, name, details = match[0], match[1], match[2], match[4]

        new_value = old_value

        if mode == "sys":
            match name:
                case "timestamp":
                    format = convert_timestamp_format(details)
                    new_value = datetime.today().strftime(format)
        elif mode == "var":
            continue

        if old_value != new_value:
            value = value.replace(old_value, new_value)

    return value    


def check_conf_file(configuration, parameters):
    for item in parameters:
        nested = "." in item["name"]

        value = None
        if(not nested and item["name"] in configuration.keys()):
            value = configuration[item["name"]]

        if(nested):
            levels = item["name"].split(".")
            value = get_nested_dict(configuration, levels, parameters, item["name"]) 

        if value == None and "default" not in item:
            raise ValueError(f"'{item['name']}' can't be empty")
        
        elif value == None and not nested:
            configuration[item["name"]] = item["default"]
            value = item["default"]

        elif value == None and nested:
            set_nested_dict(configuration, levels, item["default"])
            value = item["default"]

        value = set_variable_value(value, [])
        if(not nested):
            configuration[item["name"]] = value
        else:
            set_nested_dict(configuration, levels, value)
            
    return configuration