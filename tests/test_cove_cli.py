from io import StringIO
from typing import Any, Dict, List

import jsonlines
import pytest

from cove_cli.cove_cli import main
from tests.moto_mock_org.moto_models import SmallOrg


def test_default_behavior_just_connects(
    mock_small_org: SmallOrg, capfd: pytest.CaptureFixture
) -> None:
    main()
    results = _parse_stdout(capfd)
    assert set(r["Id"] for r in results) == set(mock_small_org.all_accounts)
    assert all(r["AssumeRoleSuccess"] for r in results)
    assert all("Results" not in r.keys() for r in results)


def _parse_stdout(capfd: pytest.CaptureFixture) -> List[Dict[str, Any]]:
    out, _ = capfd.readouterr()
    return [line for line in jsonlines.Reader(StringIO(out))]
