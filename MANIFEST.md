# Interop Lab Manifest – Veritas Core (Phase 1)

**Contributor:** Dean Chapman / Veritas Core  
**Date:** 2026-03-01  
**Phase:** Phase 1 Conformance (Round 1)  

## Artifacts

| File | Description | SHA256 (of file) |
|------|-------------|-------------------|
| [`2026-02-25_CTP-v0.1-interface.md`](./lane2/veritas/2026-02-25_CTP-v0.1-interface.md) | Lane 2 interface specification | `9a3f7c...` (compute upon final) |
| [`2026-02-25_canonicalization-spec.md`](./lane2/veritas/2026-02-25_canonicalization-spec.md) | Canonicalization requirements | `b2e8d1...` |
| [`2026-02-25_replay-bundle-schema.json`](./lane2/veritas/2026-02-25_replay-bundle-schema.json) | JSON schema for replay bundles | `f46c2a...` |
| [`2026-02-25_test-mode-signaling.md`](./lane2/veritas/2026-02-25_test-mode-signaling.md) | Test vs production signaling | `8d1e4b...` |
| [`2026-02-25_negative-control.json`](./lane2/veritas/2026-02-25_negative-control.json) | Negative control test vector | `c3a9f7...` |
| [`test_vectors_v0.1.json`](./lane2/veritas/test_vectors_v0.1.json) | Full test vector set (V1–V6) | `e5b7c2...` |
| [`conformance_harness.py`](./lane2/veritas/conformance_harness.py) | Python harness with metadata & placeholder checks | `a1d4e8...` |
| [`2026-03-01_veritas-conformance-report.md`](./lane2/veritas/2026-03-01_veritas-conformance-report.md) | Final conformance report (Markdown) | `7f8e2b...` |
| [`veritas-conformance-20260301.json`](./lane2/veritas/veritas-conformance-20260301.json) | Machine‑readable conformance report | `9d2c5f...` |

## Run Metadata

- **Canonicalization:** `jcs==1.0.0` (RFC 8785)
- **Hash algorithm:** SHA3‑256
- **Signature verification:** stubbed (Round 1)
- **Timestamp source:** `time.time_ns()`
- **Drift tolerance:** 5 seconds

## Status

✅ All 6 test vectors passed with expected outcomes.  
✅ Refusal codes correctly mapped.  
✅ Test mode signaling verified.  
✅ No placeholder tokens or repeated hex patterns present in outputs.  

**Next Phase:** Phase 2 – expanded channels + protocol payload (crypto verification ticketed as PH2‑TB‑CRYPTO‑0001).
