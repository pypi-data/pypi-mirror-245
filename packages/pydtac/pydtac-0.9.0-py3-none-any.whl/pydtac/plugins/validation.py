from pydantic import BaseModel, create_model
from typing import Type, get_type_hints

class Validator(object):
    @classmethod
    def generate_schema(cls, input_class: Type, allow_additional: bool = False) -> str:
        # Retrieve type hints from the input class
        annotations = get_type_hints(input_class)

        # Create a Pydantic model dynamically
        dynamic_model = create_model(
            'DynamicModel',
            **{name: (annotations[name], ...) for name in annotations},
            __config__=type('Config', (), {'extra': 'allow' if allow_additional else 'forbid'})
        )

        return dynamic_model.schema_json(indent=2)