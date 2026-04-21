"""Shared data model for every platform."""
from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any
from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None):
    """Forward call to original or mutated function, depending on the environment"""
    import os
    mutant_under_test = os.environ['MUTANT_UNDER_TEST']
    if mutant_under_test == 'fail':
        from mutmut.__main__ import MutmutProgrammaticFailException
        raise MutmutProgrammaticFailException('Failed programmatically')      
    elif mutant_under_test == 'stats':
        from mutmut.__main__ import record_trampoline_hit
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_'
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result
    mutant_name = mutant_under_test.rpartition('.')[-1]
    if self_arg:
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)
    return result


@dataclass
class SubStat:
    label: str
    value: int | float | str
    icon: str | None = None


@dataclass
class PlatformStats:
    platform: str
    username: str = ""
    avatar_url: str | None = None
    headline_value: str | int | float | None = None
    headline_label: str | None = None
    substats: list[SubStat] = field(default_factory=list)
    extra_fields: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "PlatformStats":
        raw_subs = data.get("substats") or []
        substats = [SubStat(**s) if isinstance(s, dict) else s for s in raw_subs]
        return cls(
            platform=data["platform"],
            username=data.get("username", ""),
            avatar_url=data.get("avatar_url"),
            headline_value=data.get("headline_value"),
            headline_label=data.get("headline_label"),
            substats=substats,
            extra_fields=dict(data.get("extra_fields") or {}),
        )

    def has_core_data(self) -> bool:
        return self.headline_value is not None or bool(self.substats) or bool(self.extra_fields)
