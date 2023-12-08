from typing import Any

from numx._parser import raise_missing_if_magic_function, parse_type_value, FUNCTION_BY_PREFIX


def _calculate_number(request: str) -> Any:
    raise_missing_if_magic_function(request)
    type_str, value = parse_type_value(request)
    return FUNCTION_BY_PREFIX[type_str](value)
