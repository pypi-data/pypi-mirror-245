import random
import traceback


def random_payload_generator(payload_schema):
    """
    The function `random_payload_generator` generates a random payload based on a given payload schema.
    
    :param payload_schema: The `payload_schema` parameter is a dictionary that represents the schema or
    structure of the payload. It contains information about the properties and their corresponding data
    types, constraints, and default values (if any). The function `random_payload_generator` generates a
    random payload based on this schema
    :return: a randomly generated payload based on the given payload schema.
    """
    try:
        rand_payload = {}
        for property, property_dict in payload_schema["properties"].items():
            if "enum" in property_dict:
                rand_payload[property] = random.choice(property_dict["enum"])
            elif "default" in property_dict:
                rand_payload[property] = property_dict["default"]
            else:
                raise Exception("Cannot generate random payload")
            
    except Exception as e:
        print(traceback.format_exc())
        
    return rand_payload