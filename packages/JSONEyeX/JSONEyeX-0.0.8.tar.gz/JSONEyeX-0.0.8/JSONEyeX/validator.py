

def jsonvalidator(schema:dict, data:dict):
    JsonValidator(schema,data)


class JsonValidator:
    def __init__(self, schema:dict, data:dict,parent_route=""):
        self.validate_schema(schema)
        self.validate_required(schema, data,parent_route)
        self.validate_data_types(schema, data,parent_route)

    @staticmethod
    def get_data_type_mapping():
        return {
            "string": str,
            "number": (int, float),
            "object": dict,
            "list": list
        }
    @staticmethod
    def validate_schema(schema):
        required_properties = ["type", "properties", "required"]
        for prop in required_properties:
            if prop not in schema:
                raise ValueError(f"'{prop}' is required in JSON schema")

        if schema["type"] != "object":
            raise ValueError("Initial type should be 'object'")
    
    @staticmethod
    def error_message(message,parent_route=""):
        error_message = message
        if parent_route:
            error_message += f" at '{parent_route}'"
        return error_message


    def validate_required(self, schema, data, parent_route):
        for prop in schema["required"]:
            if prop not in data:
                raise ValueError(self.error_message(message=f"'{prop}' is required in JSON data",parent_route=parent_route))

    def validate_data_types(self, schema, data, parent_route=""):
        for key, value in data.items():
            if key not in schema["properties"]:
                raise ValueError(self.error_message(message=f"'{key}' is not defined in JSON schema",parent_route=parent_route))

            expected_type = schema["properties"][key].get("type")
            if expected_type == "object":
                if not isinstance(value, dict):
                    raise ValueError(self.error_message(message=f"'{key}' datatype must be 'object'",parent_route=parent_route))
                new_route = f"{parent_route}.{key}" if parent_route else key
                self.__class__(schema["properties"][key], value, new_route)
            else:
                if not isinstance(value, self.get_data_type_mapping().get(expected_type, object)):
                    raise ValueError(self.error_message(message=f"'{key}' datatype must be '{expected_type}'",parent_route=parent_route))


#example 

# schema = {
#     "type": "object",
#     "properties": {
#         "name": {"type": "string"},
#         "age": {"type": "number"},
#         "address": {
#             "type": "object",
#             "properties": {
#                 "street": {"type": "string"},
#                 "city": {"type": "string"}
#             },
#             "required": ["street", "city"]
#         }
#     },
#     "required": ["name", "age", "address"]
# }

# data = {
#     "name": "John Doe",
#     "age": 30,
#     "address": {
#         "street": "123 Main St",
#         "city": "Anytown"
#     }
# }

# try:
#     validator = JsonValidator(schema, data)
#     print("No errors, validation successful.")
# except ValueError as e:
#     print(f"Validation error: {e}")
