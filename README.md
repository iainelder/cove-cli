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

## Bootstrap AWS Config

You may prefer [AWS Config](https://aws.amazon.com/config/) over cove_cli to query your inventory because it gives much faster results. But how do you know where AWS Config is enabled in the first place?

List all the configuration recorder names sorted by account region like this:

```bash
cove_cli \
'(
    s.client("config").describe_configuration_recorders()
    ["ConfigurationRecorders"][0]["name"]
)' \
--regions eu-west-1 eu-central-1 \
--target-ids 482035687842 274835020608 \
| jq -sc 'sort_by(.Id, .Region) | .[] | {Id, Region, Result}'
```

The result is the name of the account regions's recorder. A null result means the account region has no recorder. In this example only 222222222222 eu-west-1 has a recorder.

```json
{"Id":"111111111111","Region":"eu-central-1","Result":null}
{"Id":"111111111111","Region":"eu-west-1","Result":null}
{"Id":"222222222222","Region":"eu-central-1","Result":null}
{"Id":"222222222222","Region":"eu-west-1","Result":"default"}
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
