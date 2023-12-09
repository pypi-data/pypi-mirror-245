from .cache import try_cache
from .connect import send_request
from .exceptions import SampleTextNotFound, PuzzleNotAvailableError

NO_SAMPLE_TPL = """
Could not find sample input for day {day}, {year}.
The sample input is probably there, we just couldn't parse the page and find it.
Go to the webpage and grab the sample input manually (or run `advoco input`!), then
save it to a file. You can pass that file to `advoco.do` like so:

advoco.do(input_file='path/to/input.txt')
"""


@try_cache("sample_input.txt")
def get_sample_input(year: str, day: str) -> str:
    """
    Attempt to get puzzle test input from the text of the puzzle's webpage
    Eric gives a sample input for each puzzle and goes over the expected output
    using that sample.

    Fortunately, he's pretty consistent with where that sample input shows up,
    so we can take advantage and pull it down. The rules are as follows:
    We look for a <p> tag whose text includes "example" and ":" (but not
    necessarily "example:", sometimes he phrases it like, "For example,
    consider the following input:").

    We check the first such tag we find to see if it is followed by a <pre> tag
    with a <code> tag child. If so, we can feel pretty good that the contents
    of that <code> tag are our sample input.
    """
    soup = send_request("get", year, day, mmm_soup=True)

    paras = soup.find_all("p")
    for para in paras:
        para_text = para.get_text()
        if "example" in para_text and ":" in para_text:
            try:
                candidate = para.fetchNextSiblings()[0]
            except IndexError:
                break

            if candidate.name == "pre":
                for child in candidate.children:
                    if child.name == "code":
                        # We can feel pretty good that this is it
                        sample_input = child.get_text()
                        # Sample input tends to have a spare '\n' at the end
                        if sample_input.endswith("\n"):
                            return sample_input[:-1]
                        else:
                            return sample_input

            # We'd like to only check the first p tag with "example" and ":"
            break

    raise SampleTextNotFound(NO_SAMPLE_TPL.format(year=year, day=day))


@try_cache("sample_answer.txt", use_part_num=True)
def get_sample_answer(year: str, day: str, part: str) -> str:
    soup = send_request("get", year, day, mmm_soup=True)
    try:
        problem_description = soup.find_all("article")[int(part) - 1]
    except IndexError:
        raise PuzzleNotAvailableError(
            f"Part {part} of day {day}, {year} is not available"
        )
    ems = []
    for code in problem_description.find_all("code"):
        ems += code.find_all("em")
    if ems:
        return ems[-1].text

    raise SampleTextNotFound(
        f"Tried to parse the webpage for day {day}, {year} but "
        "couldn't find the sample answer"
    )
