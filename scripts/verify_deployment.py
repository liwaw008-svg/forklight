import base64
import json
import re
from pathlib import Path

from genlayer_py import create_account, create_client
from genlayer_py.chains import studionet


ROOT = Path(__file__).parents[1]
ADDRESS = "0x59Ff026b5c29eeC5d1e470310607B4Da7D4E5E94"
TRANSACTIONS = {
    "deployment": "0xd630921b46acc4eed9078046fc8ad740289ac813eabf4b7d7385ecff26971345",
    "seal": "0xe1e4d9b21c84896d813e26eff17b51b8931cd1218f4fac2bf2e8cccf2253773f",
    "illuminate": "0x98b9a85059b29097d6423ac932979c88ba677fe7c8557b8e14429201e782c23a",
}


def main() -> None:
    env = (ROOT.parents[3] / "accounts.env").read_text()
    match = re.search(
        r'^ACCOUNT_4_GENLAYER_PRIVATE_KEY\s*=\s*"?([^"\r\n]+)', env, re.M
    )
    if not match:
        raise RuntimeError("ACCOUNT_4_GENLAYER_PRIVATE_KEY is missing")
    account = create_account(account_private_key=match.group(1).strip())
    client = create_client(chain=studionet, account=account)
    transactions = {
        name: client.get_transaction(transaction_hash=tx)
        for name, tx in TRANSACTIONS.items()
    }
    deployment_source = base64.b64decode(
        transactions["deployment"]["data"]["contract_code"]
    ).decode()
    record = client.read_contract(
        address=ADDRESS,
        function_name="get_forecast",
        args=["LIVE-1789228479"],
    )
    print(
        json.dumps(
            {
                "statuses": {
                    name: {
                        "status": tx["status"],
                        "execution": tx["consensus_data"]["leader_receipt"][0][
                            "execution_result"
                        ],
                    }
                    for name, tx in transactions.items()
                },
                "walletMatches": all(
                    tx["from_address"].lower() == account.address.lower()
                    for tx in transactions.values()
                ),
                "sourceMatches": deployment_source
                == (ROOT / "contracts" / "contract.py").read_text(),
                "record": {
                    "id": record["id"],
                    "stage": record["stage"],
                    "path": record["path"],
                    "digestCount": len(record["forecast_digests"]),
                },
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
