import time
from functools import wraps


def log_execution_time(func):
    """
    Decorator that measures function execution time.
    """

    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.perf_counter()

        result = await func(*args, **kwargs)

        execution_time = time.perf_counter() - start_time

        print(
            f"[DECORATOR] {func.__name__} "
            f"executed in {execution_time:.6f} seconds"
        )

        return result

    return wrapper