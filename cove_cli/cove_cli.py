import json
import sys
from argparse import ArgumentParser
from datetime import datetime
from itertools import chain
from typing import Any, TextIO

import jsonlines
from botocove import CoveOutput, CoveSession, cove  # type: ignore[import]


class Arguments:
    code: str


def main() -> None:
    args = parse_args()
    cove_to_file(args.code, sys.stdout)


def parse_args() -> Arguments:
    parser = ArgumentParser("cove_cli")
    parser.add_argument("code", type=str, default="", nargs="?")
    return parser.parse_args(namespace=Arguments())


def cove_to_file(code: str, outfile: TextIO) -> None:
    """
    Evaluates a Python expression with CoveSession `s` in each organization
    account-region.

    Prints each account-region output as a JSON line.
    """

    def func(s: CoveSession) -> Any:
        if not code:
            return None
        return eval(code, globals(), locals())

    org_func = cove(func)
    write_jsonlines(org_func(), outfile)


def write_jsonlines(cove_output: CoveOutput, outfile: TextIO) -> None:
    """
    Writes each account-region result as a JSON line.
    """

    class Encoder(json.JSONEncoder):
        def default(self, obj: Any) -> Any:
            if isinstance(obj, Exception):
                return repr(obj)
            if isinstance(obj, datetime):
                return obj.isoformat()
            return json.JSONEncoder.default(self, obj)

    def dumps(obj: Any) -> str:
        return json.dumps(obj, cls=Encoder, indent=None)

    writer = jsonlines.Writer(fp=outfile, dumps=dumps)
    account_regions = _iter_errors_then_results(cove_output)
    writer.write_all(account_regions)


def _iter_errors_then_results(cove_output: Any) -> Any:
    """
    Returns an iterator over each account-region. First role failures, then
    exceptions, then results.
    """
    return chain(
        cove_output["FailedAssumeRole"],
        cove_output["Exceptions"],
        cove_output["Results"],
    )


if __name__ == "__main__":
    main()
