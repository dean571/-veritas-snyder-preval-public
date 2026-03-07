# Lane 3 Conformance Bundle – Application/Autonomy Stack Integration

**Date:** 2026-03-07  
**Submitter:** Dean Chapman / Veritas Core  
**Lane:** Lane 3 – Agent action request → receipt boundary  
**Version:** v0.1 (interface‑only)

## Bundle Contents
- `lane3_agent_request_v0.1.json` – Agent request schema
- `lane3_attestation_receipt_v0.1.json` – Attestation receipt schema
- `lane3_vectors_v0.1.json` – 4 conformance test vectors
- `lane3_harness.py` – Python harness (RFC 8785 canonicalization, real digest computation)
- `requirements.txt` – Dependencies
- `SHA256SUMS.txt` – File integrity hashes

## Replay Instructions
```bash
pip install -r requirements.txt
python lane3_harness.py --vectors lane3_vectors_v0.1.json --output lane3_output.jsonl
diff lane3_output.jsonl expected_output.jsonl   # should be identical

Guardrails

Interface‑only: no internal logic exposed.
Opaque digests only: no semantic parsing of policy digests.
Signature verification stubbed (Phase 1).
Canonical reason codes only (one decision enum + single primary reason_code).
Boundary Note

These artifacts define interface behavior only. Internal enforcement mechanics, circuit breaker timing, and receipt generation logic remain contributor IP. No semantic interpretation of policy digests is performed by this layer.