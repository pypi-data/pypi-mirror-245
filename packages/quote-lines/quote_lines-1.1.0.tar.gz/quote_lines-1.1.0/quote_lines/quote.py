from __future__ import annotations
import argparse
import shlex
import sys
import os


__version__ = "1.1.0"


def quote(skip_empty: bool, newline: bool, keep_trailing_newline: bool) -> None:
    # Read in stdin
    data: str = "".join(line for line in sys.stdin)
    if not keep_trailing_newline and data.endswith("\n"):
        data = data[:-1]
    # Quote lines
    items: list[str] = data.split("\n")
    if skip_empty:
        items = [i for i in items if len(i) > 0]
    quoted: list[str] = [shlex.quote(i) for i in items]
    # Output
    output: str = ("\n" if newline else " ").join(quoted)
    print(output, flush=True)


def parse_args(program: str, *args: str) -> argparse.Namespace:
    base: str = os.path.basename(program)
    parser = argparse.ArgumentParser(prog=base)
    parser.add_argument("--version", action="version", version=f"{base} {__version__}")
    parser.add_argument(
        "-n", "--newline", action="store_true", help="Output arguments with newline instead of a space as a delimiter"
    )
    parser.add_argument("--skip-empty", action="store_true", help="Do not output empty quoted strings")
    parser.add_argument(
        "--keep_trailing_newline", action="store_true", help="Do not ignore the final character if it is a newline"
    )
    return parser.parse_args(args)


def cli():
    quote(**vars(parse_args(*sys.argv)))
