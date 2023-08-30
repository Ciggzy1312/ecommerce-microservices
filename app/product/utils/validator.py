# Remove None value types in dictionaries list

def remove_none_values(payload: dict) -> dict:
    modified_payload = {}

    for key, value in payload.items():
        if value is not None:
            modified_payload[key] = value
    
    return modified_payload