from typing import Optional

from .cache import try_cache
from .connect import send_request
from .exceptions import WrongAnswerMcFly, PuzzleNotAvailableError


@try_cache("live_input.txt")
def get_live_input(year: str, day: str) -> str:
    inp = send_request("get", year, day, endpoint="/input")
    if inp.endswith("\n"):
        return inp[:-1]
    else:
        return inp


@try_cache("live_answer.txt", use_part_num=True)
def get_live_answer(year: str, day: str, part_num: str, ans: str) -> str:
    body = {"answer": ans, "level": part_num}
    soup = send_request("post", year, day, endpoint="/answer", body=body, mmm_soup=True)

    message = soup.find("article")
    if message:
        if "That's the right answer" in message.text:
            return ans
        elif "Did you already complete it" in message.text:
            old_answer = get_answer_from_puzzle_page(year, day, part_num)
            if old_answer:
                return old_answer
            else:
                raise WrongAnswerMcFly(message.text)
        else:
            raise WrongAnswerMcFly(message.text)

    raise PuzzleNotAvailableError(
        f"Tried to submit answer, but got a woogity response: {soup}"
    )


def get_answer_from_puzzle_page(year: str, day: str, part_num: str) -> Optional[str]:
    soup = send_request("get", year, day, mmm_soup=True)
    answer_texts = soup.find_all(
        lambda tag: tag.name == "p" and tag.text.startswith("Your puzzle answer was")
    )
    try:
        return answer_texts[int(part_num) - 1].find("code").text
    except IndexError:
        return None
