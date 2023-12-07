# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/04_ptyp.ipynb.

# %% auto 0
__all__ = ['StrBytes', 'NotStrBytes', 'StrQ', 'IntQ', 'notiterstr', 'isallsame']

# %% ../nbs/04_ptyp.ipynb 6
import os, inspect
from abc import abstractmethod
from functools import wraps, singledispatch

# %% ../nbs/04_ptyp.ipynb 8
from types import NoneType 
from typing import (Iterable, TypeGuard, )

# %% ../nbs/04_ptyp.ipynb 10
#| export


# %% ../nbs/04_ptyp.ipynb 12
#| export


# %% ../nbs/04_ptyp.ipynb 14
from .type import (T, )
from .util import (classname, qualname, settypes)
from .grds import (isallsame, aliascheck, trychecks, tryiter)
from .meta import (Alias, Not, Opt)

# %% ../nbs/04_ptyp.ipynb 16
@Alias(str, bytes)
class StrBytes: ...

@Not(str, bytes)
class NotStrBytes: ...

@Opt(str)
class StrQ: ...

@Opt(int)
class IntQ: ...

# %% ../nbs/04_ptyp.ipynb 17
def notiterstr(x) -> TypeGuard[Iterable[NotStrBytes]]:
    return isinstance(x, Iterable) and isinstance(x, NotStrBytes)

def isallsame(it: Iterable, dtype: type) -> TypeGuard[Iterable[T]]:
    itersafe = tryiter(it)
    if not itersafe: return trychecks(it, dtype)
    for el in it:
        if notiterstr(el) and not isallsame(el, dtype): return False
        elif not trychecks(el, dtype): return False
    return True
