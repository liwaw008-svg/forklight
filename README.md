# Forklight

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
```

The `docs/` site is a long-form editorial instrument with a real GenLayer wallet flow. Deployment metadata is added only after the published source and live transaction are verified.

