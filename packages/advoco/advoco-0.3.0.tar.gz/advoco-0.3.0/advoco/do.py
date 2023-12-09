import inspect
from copy import deepcopy
from pathlib import Path
from typing import Optional, Union

from .config import resolve_day_and_year, get_active_part
from .exceptions import PartNotDefined
from .exceptions import WrongAnswerMcFly
from .live import get_live_input, get_live_answer
from .sample import get_sample_input, get_sample_answer


class do(object):
    def __init__(
        self,
        input_file: Optional[str] = None,
        sample_input_file: Optional[str] = None,
        year: Optional[str] = None,
        day: Optional[str] = None,
        sample_answers: Optional[list[Union[str, int]]] = None,
        use_raw_input: bool = False,
        confirm: bool = False,
        no_check: bool = False,
    ):
        frame = inspect.stack()[1]
        self.caller = inspect.getmodule(frame[0])

        self.day, self.year = resolve_day_and_year(
            Path(frame.filename), year=year, day=day
        )

        try:
            self.transform_func = getattr(self.caller, "transform")
        except AttributeError:
            self.transform_func = self.default_transform

        if input_file:
            with open(input_file, "r") as infile:
                self.input = infile.read()
        else:
            self.input = get_live_input(self.year, self.day)

        if sample_input_file:
            with open(sample_input_file, "r") as infile:
                self.sample_input = infile.read()
        else:
            self.sample_input = get_sample_input(self.year, self.day)

        self.active_part = get_active_part(self.year, self.day)

        self.raw = use_raw_input
        self.sample_answer_overrides = sample_answers or []
        self.confirm = confirm
        self.no_check = no_check

        self.solve()

    def solve(self):
        if self.active_part == "1":
            # we don't move on to part 2 in the same run...nobody's THAT good at AoC
            self.do_part("1")
        else:
            self.do_part("1")
            self.do_part("2")

    def do_part(self, part_num: str):
        sample_ans = self.get_answer(part_num, self.sample_input)
        if self.no_check:
            print(f"Part {part_num} (Sample):", sample_ans)
        else:
            sample_correct = self.get_sample_answer(part_num)

            if str(sample_correct) != sample_ans:
                raise WrongAnswerMcFly(
                    f"(Sample) - Expected '{sample_correct}' but got '{sample_ans}'"
                )

            print(f"Part {part_num} (Sample): '{sample_ans}' is the correct answer!")

        live_ans = self.get_answer(part_num, self.input)
        if self.no_check:
            print(f"Part {part_num}: {live_ans}")
            return

        if self.active_part == part_num:
            if not (self.confirm or lame_confirm(live_ans, part_num)):
                return

        live_correct = get_live_answer(self.year, self.day, part_num, live_ans)
        if live_correct != live_ans:
            raise WrongAnswerMcFly(f"Expected '{live_correct}' but got '{live_ans}'")

        print(f"Part {part_num}: '{live_ans}' is the correct answer!")

    def get_answer(self, part_num: str, raw_input: str) -> str:
        if self.raw:
            input_to_use = self.transform_func(raw_input)
        else:
            input_to_use = list(
                map(lambda x: self.transform_func(x), raw_input.split("\n"))
            )

        try:
            ans = getattr(self.caller, f"part{part_num}")(deepcopy(input_to_use))
        except AttributeError:
            raise PartNotDefined(f"Part {part_num} is not defined!")

        return str(ans)

    def get_sample_answer(self, part_num):
        try:
            override = self.sample_answer_overrides[int(part_num) - 1]
            if override:
                return override
        except IndexError:
            pass

        return get_sample_answer(self.year, self.day, part_num)

    @staticmethod
    def default_transform(raw_input):
        return raw_input


def do_offline(input_file: str, use_raw_input: bool = False) -> None:
    frame = inspect.stack()[1]
    caller = inspect.getmodule(frame[0])

    with open(input_file, "r") as infile:
        raw_input = infile.read()

    try:
        transform_func = getattr(caller, "transform")
    except AttributeError:

        def transform_func(line):
            return line

    if use_raw_input:
        input_to_use = transform_func(raw_input)
    else:
        input_to_use = list(map(lambda x: transform_func(x), raw_input.split("\n")))

    for part in ["1", "2"]:
        try:
            ans = getattr(caller, f"part{part}")(deepcopy(input_to_use))
        except AttributeError:
            raise PartNotDefined(f"Part {part} is not defined!")
        else:
            print(f"Part {part} (Offline): {ans}")


def lame_confirm(ans: str, part_num: str) -> bool:
    yes = {"yes", "y", "ye", ""}
    prompt = f"Submit '{ans}' as your solution for part {part_num}? (y/n) "

    return input(prompt).lower() in yes
