# Forklight

[Open the live instrument](https://liwaw008-svg.github.io/forklight/) · [Inspect the StudioNet contract](https://explorer-studio.genlayer.com/address/0x59Ff026b5c29eeC5d1e470310607B4Da7D4E5E94)

Forklight is a GenLayer counterfactual ledger. It records a real decision as two comparable worlds—the status quo and a proposed intervention—then asks validators to inspect three independent public records and bind a forecast to exact evidence indexes and byte digests.

Unlike a one-shot recommendation, the forecast can be revisited after the intervention. A reporter attaches two new, independently hosted outcome records; a second validator round classifies what happened and whether the original forecast was accurate, overstated, or understated.

## State arc

`SEALED → FORKED → OBSERVED → CLOSED`

- `seal` records the decision frame, metric, horizon, and three distinct evidence origins.
- `illuminate` produces bounded baseline/intervention scores, a path (`ACT`, `PAUSE`, or `REDESIGN`), confidence, evidence attribution, and SHA-256 digests.
- `observe` accepts two outcome sources whose origins are distinct from each other and from the original evidence.
- `calibrate` closes the loop with an outcome and calibration result agreed by validators.

## Local verification

```bash
genvm-lint contracts/contract.py
python -m pytest -q
python scripts/verify_deployment.py
```

## Verified on StudioNet

- Contract: [`0x59Ff…5E94`](https://explorer-studio.genlayer.com/address/0x59Ff026b5c29eeC5d1e470310607B4Da7D4E5E94)
- Deployment: [`0xd630…1345`](https://explorer-studio.genlayer.com/transactions/0xd630921b46acc4eed9078046fc8ad740289ac813eabf4b7d7385ecff26971345) — FINALIZED / SUCCESS
- Live seal: [`0xe1e4…773f`](https://explorer-studio.genlayer.com/transactions/0xe1e4d9b21c84896d813e26eff17b51b8931cd1218f4fac2bf2e8cccf2253773f) — FINALIZED / SUCCESS
- Live validator forecast: [`0x98b9…c23a`](https://explorer-studio.genlayer.com/transactions/0x98b9a85059b29097d6423ac932979c88ba677fe7c8557b8e14429201e782c23a) — FINALIZED / SUCCESS
- Deployed contract source matches `contracts/contract.py` byte-for-byte.
- The live record reached `FORKED`, returned the bounded `PAUSE` path, and preserved three evidence digests.

The smoke record is explicitly a documentation-only fixture, not a real policy recommendation. Full machine-readable evidence is in [`deployment.json`](deployment.json).

The `docs/` site is a long-form editorial instrument with a two-transaction GenLayer wallet flow: seal first, then illuminate through validators. It never displays a hardcoded success state.
