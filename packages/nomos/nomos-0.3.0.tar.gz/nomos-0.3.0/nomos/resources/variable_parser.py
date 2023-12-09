from typing import Union, List, Dict, Any
import re
import json

Jsonable = Union[str, int, float, bool, List[Any], Dict[str, Any]]
VariablesData = Dict[str, Jsonable]


class VariableParser:
    _regex = r"{{\s*(.*?)\s*}}"

    @classmethod
    def populate_variables(cls, content: str, variables: VariablesData) -> str:
        def replace(match: re.Match):
            key = match.group(1)
            # Defaults to leaving the matching jinja template string
            # if no variable value is found i.e. {{ my_variable }}
            value = variables.get(key, match.group(0))
            if isinstance(value, str):
                return value
            return json.dumps(value)

        return re.sub(cls._regex, replace, content)

    @classmethod
    def find_variables(cls, content: str) -> List[str]:
        matches = re.findall(cls._regex, content)
        return matches
