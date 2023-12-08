import logging
from typing import Callable
import time
from dataclasses import dataclass, asdict

@dataclass
class TimeLog:
    kwargs: dict
    time_delta: float

def timelog(function: Callable) -> Callable:
    def wrapper(*args, **kwargs):
        if args:
            raise RuntimeError(f'Please only use kwargs for {function.__name__}{args} at {str(function.__code__).split("file")[-1].strip(">")}')
        logger = logging.getLogger(function.__name__)    
        time_start = time.perf_counter()
        r = function(**kwargs)
        time_delta = time.perf_counter() - time_start
        log = TimeLog(kwargs=kwargs, time_delta=time_delta)
        logger.debug(f'{asdict(log)}')
        return r
    return wrapper