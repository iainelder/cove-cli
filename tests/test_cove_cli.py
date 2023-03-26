from io import StringIO
from typing import Any, Dict, List
from unittest.mock import Mock, patch

import jsonlines
import pytest
from cli_test_helpers import ArgvContext, shell  # type: ignore[import]

from cove_cli.cove_cli import cove_to_file, main
from tests.moto_mock_org.moto_models import SmallOrg


def test_cli_runs_as_module():
    result = shell("python -m cove_cli --help")
    assert result.exit_code == 0


def test_cli_runs_as_command():
    result = shell("cove_cli --help")
    assert result.exit_code == 0


@patch("cove_cli.cove_cli.cove_to_file")
@pytest.mark.usefixtures("mock_small_org")
def test_cli_calls_cove_to_file(mock_cove_to_file: Mock) -> None:
    with ArgvContext("cove_cli"):
        main()
    assert mock_cove_to_file.called


def test_default_behavior_just_connects(mock_small_org: SmallOrg) -> None:
    output = _parse_cove_to_file()
    assert set(r["Id"] for r in output) == set(mock_small_org.all_accounts)
    assert all(r["AssumeRoleSuccess"] for r in output)
    assert all("Results" not in r.keys() for r in output)


def _parse_cove_to_file() -> List[Dict[str, Any]]:
    output_json = StringIO()
    cove_to_file(output_json)
    output_json.seek(0)
    return [obj for obj in jsonlines.Reader(output_json)]
