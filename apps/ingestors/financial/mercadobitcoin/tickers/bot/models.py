import json
from beanie import Document


def generate_pydantic_model(schema):
    properties = []
    required = []
    for name, data in schema['properties'].items():
        type_ = data['type']
        properties.append(f'{name}: {type_}')
        if name in schema['required']:
            required.append(name)
    properties = ',\n    '.join(properties)
    class_body = f'class Ticker(Document):\n    {properties}\n    class Config:\n        orm_mode = True'
    exec(class_body)
    return locals()['Ticker']


with open("schemas/output.json") as f:
    schema = json.load(f)


Ticker = generate_pydantic_model(schema)
