# Cove CLI

A CLI for [Botocove](https://pypi.org/project/botocove/). Collect inventory without writing boilerplate code.

Evaluates a Python expression with CoveSession `s` in each organization account-region.

Prints each account-region output as a [JSON line](https://jsonlines.org/).

Pipe the output to any other CLI tool for further processing. For example, use [jq](https://stedolan.github.io/jq/manual/) to pick out just the properties you care about.

```bash
AWS_PROFILE=sandbox-mgmt \
poetry run cove_cli 's.client("iam").list_users()["Users"]' \
| jq -c '{Id, Name, Result: [.Result[].UserName]}'
```

```json
{"Id":"111111111111","Name":"Test Account 1","UserName":["Test User A", "Test User B"]}
{"Id":"222222222222","Name":"Test Account 2","UserName":null}
{"Id":"333333333333","Name":"Test Account 3","UserName":["Test User C"]}
```

Use jq to output one JSON line for each item in the result list and output one JSON line for an empty result list.

```bash
AWS_PROFILE=sandbox-mgmt \
poetry run cove_cli 's.client("iam").list_users()["Users"]' \
| jq -c '{Id, Name} + {UserName: (.Result[].UserName // null)}'
```

```json
{"Id":"111111111111","Name":"Test Account 1","UserName":"Test User A"}
{"Id":"111111111111","Name":"Test Account 1","UserName":"Test User B"}
{"Id":"222222222222","Name":"Test Account 2","UserName":null}
{"Id":"333333333333","Name":"Test Account 3","UserName":"Test User C"}
```

## Installation

Until I package this and distribute it the normal way via PyPI, this is how I install it:

```bash
tmp="$(mktemp --dir)"
git clone https://github.com/iainelder/cove-cli.git "$tmp/cove-cli"
python3 -m venv "$tmp/venv"
source "$tmp/venv/bin/activate"
python3 -m pip install --upgrade pip
python3 -m pip install -e "$tmp/cove-cli"
cove_cli --help
```

Switch branch to get control over regions and target IDs.

```bash
git -C "$tmp/cove-cli" switch add-options
cove_cli --help
```

The options don't have unit tests yet. They work like in botocove.

```text
usage: cove_cli [-h] [--regions REGIONS [REGIONS ...]]
                [--target-ids TARGET_IDS [TARGET_IDS ...]]
                [code]

positional arguments:
  code

optional arguments:
  -h, --help            show this help message and exit
  --regions REGIONS [REGIONS ...]
  --target-ids TARGET_IDS [TARGET_IDS ...]
```
