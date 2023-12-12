from typing import Any
from typing import Dict
from typing import Sequence

from typing_extensions import TypeAlias

_K: TypeAlias = str
__all__ = (
    "similar_dict",
    "similar_sequences",
)


class ValidationError(AssertionError):
    pass


def _compare_values(actual: Any, expected: Any) -> bool:
    if isinstance(expected, type):
        if not isinstance(actual, expected):
            raise ValidationError(f"Expected type {expected}, but got {type(actual)}")
        return True
    elif isinstance(expected, dict):
        if not isinstance(actual, dict):
            raise ValidationError(f"Expected a dictionary but got {type(actual)}")
        return similar_dict(actual, expected)
    elif isinstance(expected, (list, tuple)):
        if not isinstance(actual, (list, tuple)):
            raise ValidationError(f"Expected a list or tuple, but got {type(actual)}")
        return similar_sequences(actual, expected)
    else:
        if actual != expected:
            raise ValidationError(f"{actual} != {expected}")
        return True


def similar_sequences(actual: Sequence[Any], expected_schema: Sequence[Any]) -> bool:
    if len(actual) != len(expected_schema):
        raise ValidationError(f"Expected a sequence of length {len(expected_schema)}")
    return all(
        _compare_values(actual_value, expected_schema_value)
        for actual_value, expected_schema_value in zip(actual, expected_schema)
    )


def similar_dict(actual: Dict[_K, Any], expected_schema: Dict[_K, Any]) -> bool:
    for key, expected_value in expected_schema.items():
        if key not in actual:
            raise ValidationError(f"Expected '{key}' to be present")
        _compare_values(actual[key], expected_value)

    return True
