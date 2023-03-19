import json
import sys
from datetime import datetime
from itertools import chain
from typing import Any, TextIO

import jsonlines
from botocove import CoveOutput, cove  # type: ignore[import]


def main() -> None:
    # TODO: Accept function as input à la sqlite-utils.
    org_func = cove(lambda s: None)
    write_jsonlines(org_func())


def write_jsonlines(
    cove_output: CoveOutput,
    outfile: TextIO = sys.stdout,
) -> None:
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
