import functools
import json
from pathlib import Path
from typing import Callable

ADVOCO_CACHE_DIR = Path.home() / ".cache" / "advoco"


def try_cache(fname: str, use_part_num: bool = False) -> Callable:
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(year: str, day: str, *args, **kwargs) -> str:
            if use_part_num:
                part_num = args[0]
                filename = f"{part_num}_{fname}"
            else:
                filename = fname
            cache_file = ADVOCO_CACHE_DIR / year / day / filename
            if cache_file.exists():
                with open(cache_file, "r") as infile:
                    return infile.read()
            else:
                fetched_input = func(year, day, *args, **kwargs)
                cache_file.parent.mkdir(exist_ok=True, parents=True)
                with open(cache_file, "w") as outfile:
                    outfile.write(fetched_input)
                return fetched_input

        return wrapper

    return decorator


def get_cache(year: str, day: str):
    cache_file = ADVOCO_CACHE_DIR / year / day / "cache.json"
    if cache_file.exists():
        with open(cache_file, "r") as infile:
            return json.load(infile)
    else:
        return {}


def put_cache(year: str, day: str, cache: dict):
    cache_file = ADVOCO_CACHE_DIR / year / day / "cache.json"
    with open(cache_file, "w") as outfile:
        outfile.write(json.dumps(cache))


def clear_cache(year: str = "", day: str = ""):
    if day and not year:
        raise ValueError(
            "You gave me a day and no year and that confuses me! Argle bargle!!"
        )

    to_clear = ADVOCO_CACHE_DIR

    if year:
        to_clear = to_clear / year

        if day:
            to_clear = to_clear / day

    if to_clear.exists():
        rmdir(to_clear)
    print(f"Cache entries at {to_clear} deleted")


def rmdir(directory: Path) -> None:
    directory = Path(directory)
    for item in directory.iterdir():
        if item.is_dir():
            rmdir(item)
        else:
            item.unlink()
    directory.rmdir()
