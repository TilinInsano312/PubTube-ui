"""Public scope enforcement API."""

from .checker import (
    ScopeError,
    collect_changed_paths,
    enforce_scope,
    is_high_impact_path,
    is_path_authorized,
    unauthorized_paths,
)

__all__ = [
    "ScopeError",
    "collect_changed_paths",
    "enforce_scope",
    "is_high_impact_path",
    "is_path_authorized",
    "unauthorized_paths",
]
