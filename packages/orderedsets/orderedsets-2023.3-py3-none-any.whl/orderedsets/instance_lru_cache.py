from functools import cached_property, lru_cache, partial, update_wrapper
from typing import Callable, Optional, TypeVar, Union

T = TypeVar("T")

def instance_lru_cache(
    method: Optional[Callable[..., T]] = None,
    *,
    maxsize: Optional[int] = 16,
    typed: bool = False
) -> Union[Callable[..., T], Callable[[Callable[..., T]], Callable[..., T]]]:
    """Least-recently-used cache decorator for instance methods.

    The cache follows the lifetime of an object (it is stored on the object,
    not on the class) and can be used on unhashable objects. Wrapper around
    functools.lru_cache.

    If *maxsize* is set to None, the LRU features are disabled and the cache
    can grow without bound.

    If *typed* is True, arguments of different types will be cached separately.
    For example, f(3.0) and f(3) will be treated as distinct calls with
    distinct results.

    Arguments to the cached method (other than 'self') must be hashable.

    View the cache statistics named tuple (hits, misses, maxsize, currsize)
    with f.cache_info().  Clear the cache and statistics with f.cache_clear().
    Access the underlying function with f.__wrapped__.

    """

    def decorator(wrapped: Callable[..., T]) -> cached_property[Callable[..., T]]:
        def wrapper(self: object) -> Callable[..., T]:
            return lru_cache(maxsize=maxsize, typed=typed)(
                update_wrapper(partial(wrapped, self), wrapped)
            )

        return cached_property(wrapper)  ## type: ignore

    return decorator if method is None else decorator(method)
