"""Small text/number helpers shared by providers and the renderer."""
from __future__ import annotations

import re


_NUM_RE = re.compile(r"[-+]?\d[\d,]*(?:\.\d+)?")
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


def x_parse_int__mutmut_orig(text: str | None) -> int | None:
    if text is None:
        return None
    m = _NUM_RE.search(str(text))
    if not m:
        return None
    try:
        return int(m.group(0).replace(",", "").split(".")[0])
    except ValueError:
        return None


def x_parse_int__mutmut_1(text: str | None) -> int | None:
    if text is not None:
        return None
    m = _NUM_RE.search(str(text))
    if not m:
        return None
    try:
        return int(m.group(0).replace(",", "").split(".")[0])
    except ValueError:
        return None


def x_parse_int__mutmut_2(text: str | None) -> int | None:
    if text is None:
        return None
    m = None
    if not m:
        return None
    try:
        return int(m.group(0).replace(",", "").split(".")[0])
    except ValueError:
        return None


def x_parse_int__mutmut_3(text: str | None) -> int | None:
    if text is None:
        return None
    m = _NUM_RE.search(None)
    if not m:
        return None
    try:
        return int(m.group(0).replace(",", "").split(".")[0])
    except ValueError:
        return None


def x_parse_int__mutmut_4(text: str | None) -> int | None:
    if text is None:
        return None
    m = _NUM_RE.search(str(None))
    if not m:
        return None
    try:
        return int(m.group(0).replace(",", "").split(".")[0])
    except ValueError:
        return None


def x_parse_int__mutmut_5(text: str | None) -> int | None:
    if text is None:
        return None
    m = _NUM_RE.search(str(text))
    if m:
        return None
    try:
        return int(m.group(0).replace(",", "").split(".")[0])
    except ValueError:
        return None


def x_parse_int__mutmut_6(text: str | None) -> int | None:
    if text is None:
        return None
    m = _NUM_RE.search(str(text))
    if not m:
        return None
    try:
        return int(None)
    except ValueError:
        return None


def x_parse_int__mutmut_7(text: str | None) -> int | None:
    if text is None:
        return None
    m = _NUM_RE.search(str(text))
    if not m:
        return None
    try:
        return int(m.group(0).replace(",", "").split(None)[0])
    except ValueError:
        return None


def x_parse_int__mutmut_8(text: str | None) -> int | None:
    if text is None:
        return None
    m = _NUM_RE.search(str(text))
    if not m:
        return None
    try:
        return int(m.group(0).replace(None, "").split(".")[0])
    except ValueError:
        return None


def x_parse_int__mutmut_9(text: str | None) -> int | None:
    if text is None:
        return None
    m = _NUM_RE.search(str(text))
    if not m:
        return None
    try:
        return int(m.group(0).replace(",", None).split(".")[0])
    except ValueError:
        return None


def x_parse_int__mutmut_10(text: str | None) -> int | None:
    if text is None:
        return None
    m = _NUM_RE.search(str(text))
    if not m:
        return None
    try:
        return int(m.group(0).replace("").split(".")[0])
    except ValueError:
        return None


def x_parse_int__mutmut_11(text: str | None) -> int | None:
    if text is None:
        return None
    m = _NUM_RE.search(str(text))
    if not m:
        return None
    try:
        return int(m.group(0).replace(",", ).split(".")[0])
    except ValueError:
        return None


def x_parse_int__mutmut_12(text: str | None) -> int | None:
    if text is None:
        return None
    m = _NUM_RE.search(str(text))
    if not m:
        return None
    try:
        return int(m.group(None).replace(",", "").split(".")[0])
    except ValueError:
        return None


def x_parse_int__mutmut_13(text: str | None) -> int | None:
    if text is None:
        return None
    m = _NUM_RE.search(str(text))
    if not m:
        return None
    try:
        return int(m.group(1).replace(",", "").split(".")[0])
    except ValueError:
        return None


def x_parse_int__mutmut_14(text: str | None) -> int | None:
    if text is None:
        return None
    m = _NUM_RE.search(str(text))
    if not m:
        return None
    try:
        return int(m.group(0).replace("XX,XX", "").split(".")[0])
    except ValueError:
        return None


def x_parse_int__mutmut_15(text: str | None) -> int | None:
    if text is None:
        return None
    m = _NUM_RE.search(str(text))
    if not m:
        return None
    try:
        return int(m.group(0).replace(",", "XXXX").split(".")[0])
    except ValueError:
        return None


def x_parse_int__mutmut_16(text: str | None) -> int | None:
    if text is None:
        return None
    m = _NUM_RE.search(str(text))
    if not m:
        return None
    try:
        return int(m.group(0).replace(",", "").split("XX.XX")[0])
    except ValueError:
        return None


def x_parse_int__mutmut_17(text: str | None) -> int | None:
    if text is None:
        return None
    m = _NUM_RE.search(str(text))
    if not m:
        return None
    try:
        return int(m.group(0).replace(",", "").split(".")[1])
    except ValueError:
        return None

x_parse_int__mutmut_mutants : ClassVar[MutantDict] = {
'x_parse_int__mutmut_1': x_parse_int__mutmut_1, 
    'x_parse_int__mutmut_2': x_parse_int__mutmut_2, 
    'x_parse_int__mutmut_3': x_parse_int__mutmut_3, 
    'x_parse_int__mutmut_4': x_parse_int__mutmut_4, 
    'x_parse_int__mutmut_5': x_parse_int__mutmut_5, 
    'x_parse_int__mutmut_6': x_parse_int__mutmut_6, 
    'x_parse_int__mutmut_7': x_parse_int__mutmut_7, 
    'x_parse_int__mutmut_8': x_parse_int__mutmut_8, 
    'x_parse_int__mutmut_9': x_parse_int__mutmut_9, 
    'x_parse_int__mutmut_10': x_parse_int__mutmut_10, 
    'x_parse_int__mutmut_11': x_parse_int__mutmut_11, 
    'x_parse_int__mutmut_12': x_parse_int__mutmut_12, 
    'x_parse_int__mutmut_13': x_parse_int__mutmut_13, 
    'x_parse_int__mutmut_14': x_parse_int__mutmut_14, 
    'x_parse_int__mutmut_15': x_parse_int__mutmut_15, 
    'x_parse_int__mutmut_16': x_parse_int__mutmut_16, 
    'x_parse_int__mutmut_17': x_parse_int__mutmut_17
}

def parse_int(*args, **kwargs):
    result = _mutmut_trampoline(x_parse_int__mutmut_orig, x_parse_int__mutmut_mutants, args, kwargs)
    return result 

parse_int.__signature__ = _mutmut_signature(x_parse_int__mutmut_orig)
x_parse_int__mutmut_orig.__name__ = 'x_parse_int'


def x_parse_float__mutmut_orig(text: str | None) -> float | None:
    if text is None:
        return None
    m = _NUM_RE.search(str(text))
    if not m:
        return None
    try:
        return float(m.group(0).replace(",", ""))
    except ValueError:
        return None


def x_parse_float__mutmut_1(text: str | None) -> float | None:
    if text is not None:
        return None
    m = _NUM_RE.search(str(text))
    if not m:
        return None
    try:
        return float(m.group(0).replace(",", ""))
    except ValueError:
        return None


def x_parse_float__mutmut_2(text: str | None) -> float | None:
    if text is None:
        return None
    m = None
    if not m:
        return None
    try:
        return float(m.group(0).replace(",", ""))
    except ValueError:
        return None


def x_parse_float__mutmut_3(text: str | None) -> float | None:
    if text is None:
        return None
    m = _NUM_RE.search(None)
    if not m:
        return None
    try:
        return float(m.group(0).replace(",", ""))
    except ValueError:
        return None


def x_parse_float__mutmut_4(text: str | None) -> float | None:
    if text is None:
        return None
    m = _NUM_RE.search(str(None))
    if not m:
        return None
    try:
        return float(m.group(0).replace(",", ""))
    except ValueError:
        return None


def x_parse_float__mutmut_5(text: str | None) -> float | None:
    if text is None:
        return None
    m = _NUM_RE.search(str(text))
    if m:
        return None
    try:
        return float(m.group(0).replace(",", ""))
    except ValueError:
        return None


def x_parse_float__mutmut_6(text: str | None) -> float | None:
    if text is None:
        return None
    m = _NUM_RE.search(str(text))
    if not m:
        return None
    try:
        return float(None)
    except ValueError:
        return None


def x_parse_float__mutmut_7(text: str | None) -> float | None:
    if text is None:
        return None
    m = _NUM_RE.search(str(text))
    if not m:
        return None
    try:
        return float(m.group(0).replace(None, ""))
    except ValueError:
        return None


def x_parse_float__mutmut_8(text: str | None) -> float | None:
    if text is None:
        return None
    m = _NUM_RE.search(str(text))
    if not m:
        return None
    try:
        return float(m.group(0).replace(",", None))
    except ValueError:
        return None


def x_parse_float__mutmut_9(text: str | None) -> float | None:
    if text is None:
        return None
    m = _NUM_RE.search(str(text))
    if not m:
        return None
    try:
        return float(m.group(0).replace(""))
    except ValueError:
        return None


def x_parse_float__mutmut_10(text: str | None) -> float | None:
    if text is None:
        return None
    m = _NUM_RE.search(str(text))
    if not m:
        return None
    try:
        return float(m.group(0).replace(",", ))
    except ValueError:
        return None


def x_parse_float__mutmut_11(text: str | None) -> float | None:
    if text is None:
        return None
    m = _NUM_RE.search(str(text))
    if not m:
        return None
    try:
        return float(m.group(None).replace(",", ""))
    except ValueError:
        return None


def x_parse_float__mutmut_12(text: str | None) -> float | None:
    if text is None:
        return None
    m = _NUM_RE.search(str(text))
    if not m:
        return None
    try:
        return float(m.group(1).replace(",", ""))
    except ValueError:
        return None


def x_parse_float__mutmut_13(text: str | None) -> float | None:
    if text is None:
        return None
    m = _NUM_RE.search(str(text))
    if not m:
        return None
    try:
        return float(m.group(0).replace("XX,XX", ""))
    except ValueError:
        return None


def x_parse_float__mutmut_14(text: str | None) -> float | None:
    if text is None:
        return None
    m = _NUM_RE.search(str(text))
    if not m:
        return None
    try:
        return float(m.group(0).replace(",", "XXXX"))
    except ValueError:
        return None

x_parse_float__mutmut_mutants : ClassVar[MutantDict] = {
'x_parse_float__mutmut_1': x_parse_float__mutmut_1, 
    'x_parse_float__mutmut_2': x_parse_float__mutmut_2, 
    'x_parse_float__mutmut_3': x_parse_float__mutmut_3, 
    'x_parse_float__mutmut_4': x_parse_float__mutmut_4, 
    'x_parse_float__mutmut_5': x_parse_float__mutmut_5, 
    'x_parse_float__mutmut_6': x_parse_float__mutmut_6, 
    'x_parse_float__mutmut_7': x_parse_float__mutmut_7, 
    'x_parse_float__mutmut_8': x_parse_float__mutmut_8, 
    'x_parse_float__mutmut_9': x_parse_float__mutmut_9, 
    'x_parse_float__mutmut_10': x_parse_float__mutmut_10, 
    'x_parse_float__mutmut_11': x_parse_float__mutmut_11, 
    'x_parse_float__mutmut_12': x_parse_float__mutmut_12, 
    'x_parse_float__mutmut_13': x_parse_float__mutmut_13, 
    'x_parse_float__mutmut_14': x_parse_float__mutmut_14
}

def parse_float(*args, **kwargs):
    result = _mutmut_trampoline(x_parse_float__mutmut_orig, x_parse_float__mutmut_mutants, args, kwargs)
    return result 

parse_float.__signature__ = _mutmut_signature(x_parse_float__mutmut_orig)
x_parse_float__mutmut_orig.__name__ = 'x_parse_float'


def x_format_int__mutmut_orig(value) -> str:
    try:
        return f"{int(value):,}"
    except (TypeError, ValueError):
        return "--"


def x_format_int__mutmut_1(value) -> str:
    try:
        return f"{int(None):,}"
    except (TypeError, ValueError):
        return "--"


def x_format_int__mutmut_2(value) -> str:
    try:
        return f"{int(value):,}"
    except (TypeError, ValueError):
        return "XX--XX"

x_format_int__mutmut_mutants : ClassVar[MutantDict] = {
'x_format_int__mutmut_1': x_format_int__mutmut_1, 
    'x_format_int__mutmut_2': x_format_int__mutmut_2
}

def format_int(*args, **kwargs):
    result = _mutmut_trampoline(x_format_int__mutmut_orig, x_format_int__mutmut_mutants, args, kwargs)
    return result 

format_int.__signature__ = _mutmut_signature(x_format_int__mutmut_orig)
x_format_int__mutmut_orig.__name__ = 'x_format_int'


def x_format_ratio__mutmut_orig(value, decimals: int = 2) -> str:
    try:
        return f"{float(value):.{decimals}f}"
    except (TypeError, ValueError):
        return "--"


def x_format_ratio__mutmut_1(value, decimals: int = 3) -> str:
    try:
        return f"{float(value):.{decimals}f}"
    except (TypeError, ValueError):
        return "--"


def x_format_ratio__mutmut_2(value, decimals: int = 2) -> str:
    try:
        return f"{float(None):.{decimals}f}"
    except (TypeError, ValueError):
        return "--"


def x_format_ratio__mutmut_3(value, decimals: int = 2) -> str:
    try:
        return f"{float(value):.{decimals}f}"
    except (TypeError, ValueError):
        return "XX--XX"

x_format_ratio__mutmut_mutants : ClassVar[MutantDict] = {
'x_format_ratio__mutmut_1': x_format_ratio__mutmut_1, 
    'x_format_ratio__mutmut_2': x_format_ratio__mutmut_2, 
    'x_format_ratio__mutmut_3': x_format_ratio__mutmut_3
}

def format_ratio(*args, **kwargs):
    result = _mutmut_trampoline(x_format_ratio__mutmut_orig, x_format_ratio__mutmut_mutants, args, kwargs)
    return result 

format_ratio.__signature__ = _mutmut_signature(x_format_ratio__mutmut_orig)
x_format_ratio__mutmut_orig.__name__ = 'x_format_ratio'


def x_clamp__mutmut_orig(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def x_clamp__mutmut_1(value: float, low: float, high: float) -> float:
    return max(None, min(high, value))


def x_clamp__mutmut_2(value: float, low: float, high: float) -> float:
    return max(low, None)


def x_clamp__mutmut_3(value: float, low: float, high: float) -> float:
    return max(min(high, value))


def x_clamp__mutmut_4(value: float, low: float, high: float) -> float:
    return max(low, )


def x_clamp__mutmut_5(value: float, low: float, high: float) -> float:
    return max(low, min(None, value))


def x_clamp__mutmut_6(value: float, low: float, high: float) -> float:
    return max(low, min(high, None))


def x_clamp__mutmut_7(value: float, low: float, high: float) -> float:
    return max(low, min(value))


def x_clamp__mutmut_8(value: float, low: float, high: float) -> float:
    return max(low, min(high, ))

x_clamp__mutmut_mutants : ClassVar[MutantDict] = {
'x_clamp__mutmut_1': x_clamp__mutmut_1, 
    'x_clamp__mutmut_2': x_clamp__mutmut_2, 
    'x_clamp__mutmut_3': x_clamp__mutmut_3, 
    'x_clamp__mutmut_4': x_clamp__mutmut_4, 
    'x_clamp__mutmut_5': x_clamp__mutmut_5, 
    'x_clamp__mutmut_6': x_clamp__mutmut_6, 
    'x_clamp__mutmut_7': x_clamp__mutmut_7, 
    'x_clamp__mutmut_8': x_clamp__mutmut_8
}

def clamp(*args, **kwargs):
    result = _mutmut_trampoline(x_clamp__mutmut_orig, x_clamp__mutmut_mutants, args, kwargs)
    return result 

clamp.__signature__ = _mutmut_signature(x_clamp__mutmut_orig)
x_clamp__mutmut_orig.__name__ = 'x_clamp'
