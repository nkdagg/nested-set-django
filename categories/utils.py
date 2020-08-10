import json

def extract_values_from_ord_dicts(list_of_ordered_dicts):
    # Extract values from ordered dictionaries returned by SQL requests
    lis = []
    for inner_dict in list_of_ordered_dicts:
        lis.append({k:inner_dict[k] for k in ('id','name') if k in inner_dict})
    return lis


def prepare_categories_data(data):
    # Traverses the JSON data from POST request: 
    # Creates parent, left and right values for the Nested Set-like model
    # Outputs prepared structure to push to the database
    path = 1
    data_dump = {}

    def prepare(data, parent):
        nonlocal path, data_dump
        if(isinstance(data, dict)):
            data_dump[data["name"]] = {"parent": parent, "lft": path}
            path += 1
            prepare(data.get("children"), data["name"])
            data_dump[data["name"]]["rgt"] = path
            path += 1
        elif(isinstance(data, list)):
            for point in data:
                prepare(point, parent)

    prepare(data, "none")
    return data_dump


def validate_json(json_data):
    try:
        return json.loads(json_data)
    except json.decoder.JSONDecodeError as e:
        print("Invalid JSON") 
        raise e from None
    else:
        print("Valid JSON") 


def validate_input_data(data):
    structure = {
        'name': str,
        'children': list
    }
    def check_structure(struct, conf):
        if isinstance(struct, dict) and isinstance(conf, dict):
            return all(k in conf and check_structure(struct[k], conf[k]) for k in struct)
        if isinstance(struct, list) and isinstance(conf, list):
            return all(check_structure(struct[0], c) for c in conf)
        elif isinstance(struct, conf): 
            return isinstance(conf, type)
        else:
            raise ValueError
    