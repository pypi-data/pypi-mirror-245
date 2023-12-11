from typing import Any
from typing import Dict
from typing import Sequence

from typing_extensions import TypeAlias

_K: TypeAlias = str
__all__ = (
    "similar_dict",
    "similar_sequences",
)


def _compare_values(actual: Any, expected: Any) -> bool:
    if isinstance(expected, type):
        return isinstance(actual, expected)
    elif isinstance(expected, dict):
        return isinstance(actual, dict) and similar_dict(actual, expected)
    elif isinstance(expected, (list, tuple)):
        return isinstance(actual, (list, tuple)) and similar_sequences(actual, expected)
    else:
        return actual == expected


def similar_sequences(actual: Sequence[Any], expected_schema: Sequence[Any]) -> bool:
    if len(actual) != len(expected_schema):
        return False
    return all(
        _compare_values(actual_value, expected_schema_value)
        for actual_value, expected_schema_value in zip(actual, expected_schema)
    )


def similar_dict(actual: Dict[_K, Any], expected_schema: Dict[_K, Any]) -> bool:
    for key, expected_value in expected_schema.items():
        if key not in actual:
            return False
        if not _compare_values(actual[key], expected_value):
            return False
    return True
