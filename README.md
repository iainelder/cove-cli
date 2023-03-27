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
