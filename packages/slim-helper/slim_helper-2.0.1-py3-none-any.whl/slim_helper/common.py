import time
import sys
from typing import Callable, Any


def retry(times: int, interval_secs: int):
    """retry

    Args:
        times (int): number of retries
        delay_secs (int): retry interval
    """

    def decorator(func):
        def warpper(*args, **kwargs):
            attempt = 0
            while attempt < times:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(
                        f"error: retry().exception thrown {e} when attempting to run {func}({args}&{kwargs}), attempt {attempt} of {times}",
                        file=sys.stderr,
                    )
                    attempt += 1
                    time.sleep(interval_secs)
            return func(*args, **kwargs)

        return warpper

    return decorator


def timer(func: Callable):
    """timer

    Args:
        func (Callable): target function
    """

    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        total = end_time - start_time
        print(f"execution seconds of {func.__name__} is {total:.3f}")
        return result

    return wrapper


def nvl(*args) -> Any | None:
    """null value logic"""
    r = None
    for a in args:
        r = a
        if r is not None:
            break
    return r
