import json
import re
from pathlib import Path

from genlayer_py import create_account, create_client
from genlayer_py.chains import studionet


ROOT = Path(__file__).parents[1]
ENV = ROOT.parents[3] / "accounts.env"


def main() -> None:
    match = re.search(
        r'^ACCOUNT_4_GENLAYER_PRIVATE_KEY\s*=\s*"?([^"\r\n]+)',
        ENV.read_text(),
        re.M,
    )
    if not match:
        raise RuntimeError("ACCOUNT_4_GENLAYER_PRIVATE_KEY is missing")

    account = create_account(account_private_key=match.group(1).strip())
    client = create_client(chain=studionet, account=account)
    transaction = client.deploy_contract(
        code=(ROOT / "contracts" / "contract.py").read_text(), args=[]
    )
    print("deployment_tx=" + str(transaction), flush=True)
    receipt = client.wait_for_transaction_receipt(
        transaction_hash=transaction,
        status="ACCEPTED",
        retries=120,
        interval=10000,
    )
    address = receipt.get("data", {}).get("contract_address")
    if not address:
        raise RuntimeError("deployment address missing")
    print(
        json.dumps(
            {
                "contract": address,
                "deploymentTx": transaction,
                "network": "StudioNet",
                "status": receipt.get("status_name"),
                "result": receipt.get("result_name"),
            },
            default=str,
        ),
        flush=True,
    )


if __name__ == "__main__":
    main()
