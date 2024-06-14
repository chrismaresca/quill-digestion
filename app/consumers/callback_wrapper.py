from typing import Dict, Any, Callable
from functools import wraps


def callback_wrapper(callback: Callable):
    """
    Decorator to wrap a callback function for passing additional args.
    """
    @wraps(callback)
    async def wrapper(event: Dict[str, Any], *args, **kwargs):
        try:
            print(f"Processing event: {event}")
            await callback(event, *args, **kwargs)
        except Exception as e:
            print(f"Error processing event: {event} - {e}")
            raise
    return wrapper