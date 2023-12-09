from pathlib import Path

import click

from advoco import __version__
from advoco.cache import clear_cache
from advoco.config import resolve_day_and_year, get_active_part
from advoco.live import get_live_input
from advoco.sample import get_sample_answer, get_sample_input

SCRIPT_CONTENT = """import advoco


def transform(line):
    return line


def part1(inp):
    return "Not implemented"


def part2(inp):
    return "Not implemented"


advoco.do()
"""


@click.group()
@click.version_option(version=__version__, prog_name="Advoco")
def cli():
    pass


@click.command(name="generate", short_help="Generate python file for day")
@click.option("-d", "--day", help="Day to generate")
@click.option("--output-file", help="Name of file to which to write script")
def generate(day, output_file):
    if not output_file:
        context = Path.cwd()
        day, _ = resolve_day_and_year(context, day=day)
        output_file = f"{day}.py"

    if not Path(output_file).exists() or click.confirm(
        f"{output_file} already exists! Overwrite?"
    ):
        with open(output_file, "w") as outfile:
            outfile.write(SCRIPT_CONTENT)

        click.echo(f"Script written to {output_file}. Happy adventing!")


@click.command(name="generate-year", short_help="Generate folder structure for year")
@click.option("--folder-name", help="Name of folder to generate")
@click.option("-y", "--year", help="Year to generate folder for")
def generate_year(folder_name, year):
    context = Path.cwd()
    _, year = resolve_day_and_year(context, year=year, day="1")
    folder_name = folder_name or year

    day_one = context / folder_name / "1.py"
    day_one.parent.mkdir()

    with open(day_one, "w") as outfile:
        outfile.write(SCRIPT_CONTENT)

    click.echo(f"New year folder created at ./{folder_name}")
    click.echo(f"First day's script written to ./{folder_name}/1.py")
    click.echo("Happy Adventing!")


@click.command(name="input", short_help="Get input")
@click.option("-d", "--day", help="Day to fetch input for")
@click.option("-y", "--year", help="Year to fetch input for")
@click.option("-s", "--sample", is_flag=True, help="Fetch sample input")
def get_input(day, year, sample):
    context = Path.cwd()
    day, year = resolve_day_and_year(context, day=day, year=year)
    raw_input = get_sample_input(year, day) if sample else get_live_input(year, day)
    click.echo(raw_input)


@click.command(name="clear-cache", short_help="Delete cache entries")
@click.option("-d", "--day", default="", help="Delete this day's folder in cache")
@click.option("-y", "--year", default="", help="Delete this year's folder in cahce")
def clear_cache_cmd(day, year):
    clear_cache(year, day)


@click.command(name="sample-output", short_help="Get sample output")
@click.option("-d", "--day", help="Day to fetch output for")
@click.option("-y", "--year", help="Year to fetch output for")
@click.option("-p", "--part", default="1", help="Puzzle part to fetch output for")
def sample_output(day, year, part):
    context = Path.cwd()
    day, year = resolve_day_and_year(context, day=day, year=year)
    click.echo(get_sample_answer(year, day, part))


@click.command(name="status", short_help="View day status")
@click.option("-d", "--day", default="", help="Day to fetch status for")
@click.option("-y", "--year", default="", help="Year to fetch status for")
def status_cmd(day, year):
    active_part = get_active_part(year, day)
    if active_part == "-1":
        click.echo(f"Congratulations! You've completed {year}, Day {day}")
    else:
        click.echo(f"You're working on Part {active_part} for {year}, Day {day}")


cli.add_command(generate)
cli.add_command(generate_year)
cli.add_command(get_input)
cli.add_command(clear_cache_cmd)
cli.add_command(sample_output)
cli.add_command(status_cmd)
