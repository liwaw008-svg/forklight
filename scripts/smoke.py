import json
import re
import time
from pathlib import Path

from genlayer_py import create_account, create_client
from genlayer_py.chains import studionet


ROOT = Path(__file__).parents[1]
ADDRESS = "0x5a25c18d8e33447766c625D94cAD02e12bcB0Bf4"


def client_for_account():
    env = (ROOT.parents[3] / "accounts.env").read_text()
    match = re.search(
        r'^ACCOUNT_4_GENLAYER_PRIVATE_KEY\s*=\s*"?([^"\r\n]+)', env, re.M
    )
    if not match:
        raise RuntimeError("ACCOUNT_4_GENLAYER_PRIVATE_KEY is missing")
    return create_client(
        chain=studionet,
        account=create_account(account_private_key=match.group(1).strip()),
    )


def main() -> None:
    client = client_for_account()
    forecast_id = "LIVE-" + str(int(time.time()))
    seal_tx = client.write_contract(
        address=ADDRESS,
        function_name="seal",
        args=[
            forecast_id,
            "Evaluate a documentation-only routing policy fixture.",
            "Continue using the existing documented routing convention.",
            "Adopt the alternate documented routing convention for evaluation.",
            "Completeness of the published routing documentation.",
            "One technical verification cycle after the fixture is recorded.",
            [
                "https://www.iana.org/domains/reserved",
                "https://www.rfc-editor.org/rfc/rfc2606.txt",
                "https://example.com/",
            ],
        ],
        value=0,
    )
    seal_receipt = client.wait_for_transaction_receipt(
        transaction_hash=seal_tx, status="ACCEPTED", retries=120, interval=5000
    )
    illuminate_tx = client.write_contract(
        address=ADDRESS,
        function_name="illuminate",
        args=[forecast_id],
        value=0,
    )
    illuminate_receipt = client.wait_for_transaction_receipt(
        transaction_hash=illuminate_tx,
        status="ACCEPTED",
        retries=120,
        interval=5000,
    )
    record = client.read_contract(
        address=ADDRESS, function_name="get_forecast", args=[forecast_id]
    )
    print(
        json.dumps(
            {
                "recordId": forecast_id,
                "sealTx": seal_tx,
                "sealStatus": seal_receipt.get("status_name"),
                "sealResult": seal_receipt.get("result_name"),
                "illuminateTx": illuminate_tx,
                "illuminateStatus": illuminate_receipt.get("status_name"),
                "illuminateResult": illuminate_receipt.get("result_name"),
                "stage": record["stage"],
                "path": record["path"],
                "digestCount": len(record["forecast_digests"]),
            },
            default=str,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
