"""Módulo para gerenciar deprecações no sistema."""
import warnings
import functools
from typing import Callable, TypeVar, ParamSpec, Any

P = ParamSpec('P')
R = TypeVar('R')

def deprecated(reason: str) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """
    Decorator para marcar funções/classes como deprecated.
    
    Args:
        reason: Motivo da deprecação e sugestão de alternativa
        
    Returns:
        Callable: Decorator function
    """
    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            warnings.warn(
                f"{func.__name__} is deprecated. {reason}",
                category=DeprecationWarning,
                stacklevel=2
            )
            return func(*args, **kwargs)
        return wrapper
    return decorator 