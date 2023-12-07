import warnings

from .add_validation_rules import AddValidationRules
from .base_extension import LifecycleStep, SchemaExtension
from .disable_validation import DisableValidation
from .field_extension import FieldExtension
from .mask_errors import MaskErrors
from .max_aliases import MaxAliasesLimiter
from .max_tokens import MaxTokensLimiter
from .parser_cache import ParserCache
from .query_depth_limiter import IgnoreContext, QueryDepthLimiter
from .validation_cache import ValidationCache


def __getattr__(name: str):
    if name == "Extension":
        warnings.warn(
            (
                "importing `Extension` from `strawberry.extensions` "
                "is deprecated, import `SchemaExtension` instead."
            ),
            DeprecationWarning,
            stacklevel=2,
        )
        return SchemaExtension

    raise AttributeError(f"module {__name__} has no attribute {name}")


__all__ = [
    "FieldExtension",
    "SchemaExtension",
    "LifecycleStep",
    "AddValidationRules",
    "DisableValidation",
    "ParserCache",
    "QueryDepthLimiter",
    "IgnoreContext",
    "ValidationCache",
    "MaskErrors",
    "MaxAliasesLimiter",
    "MaxTokensLimiter",
]
