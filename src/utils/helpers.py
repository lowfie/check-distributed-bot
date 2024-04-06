import re
from datetime import datetime


def to_lower_camel(string: str) -> str:
    return "".join(
        word.capitalize() if i > 0 else word for i, word in enumerate(string.split("_"))
    )


def to_underscore_lower_case(string: str):
    names = re.split("(?=[A-Z])", string)
    return "_".join([x.lower() for x in names if x])


def format_timedelta(seconds: int):
    if not seconds:
        return None

    seconds = datetime.now().timestamp() - seconds
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{int(hours)}h{int(minutes)}m"
